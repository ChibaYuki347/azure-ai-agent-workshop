# オブザーバビリティ トレーシング ハンズオン ガイド

この手順書では、`samples/python/06_observability_tracing/main.py` をローカルで実行し、OpenTelemetry のトレースを Azure Monitor (Application Insights) に送信して可視化する方法を説明します。ワークショップ受講中に、ご自身の環境で同じ流れを再現してください。

## 1. 前提条件

開始前に次の項目を準備します。

- **Azure サブスクリプション** と Azure AI Foundry プロジェクト
- **モデル デプロイ** (例: `gpt-4o-mini`) がプロジェクトの **Models + Endpoints** に存在
- トレースを送信する **Application Insights** リソースまたは接続文字列
- **Azure CLI** をインストールし `az login` 済み
- **Python 3.10 以上**
- 本リポジトリへのアクセス (クローンまたは ZIP 展開)

> 💡 **認証について**: サンプルは `DefaultAzureCredential` を使用します。ローカル開発では `az login` が最も簡単です。別の認証方法を使う場合は、対象の Azure AI Foundry プロジェクトにアクセス権があることを確認してください。

## 2. リポジトリのセットアップ

1. ターミナルで Python サンプル ディレクトリへ移動します。

    ```bash
    cd samples/python
    ```

2. 仮想環境を作成し、有効化します。

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # PowerShell の場合: .venv\Scripts\Activate.ps1
    ```

3. 依存パッケージをインストールします。

    ```bash
    pip install -r requirements.txt
    ```

## 3. 環境変数の設定

サンプルは環境変数から設定を読み込みます。`.env` を作成するか、シェルでエクスポートしてください。

| 変数名 | 必須 | 説明 |
| --- | --- | --- |
| `PROJECT_ENDPOINT` | ✅ | プロジェクトのエンドポイント例: `https://<resource>.services.ai.azure.com/api/projects/<project>` |
| `MODEL_DEPLOYMENT_NAME` | ✅ | 利用するモデル デプロイ名 (`gpt-4o-mini` など) |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | 任意 (推奨) | エクスポーターで使用する Application Insights の接続文字列 |
| `ENABLE_AGENT_TRACE_CONTENT` | 任意 | `true` にするとメッセージ本文をトレースに含める |

> 🔐 **ポイント**: 接続文字列はリポジトリに含めないでください。シェルでエクスポートするか、`direnv`・`dotenv` などのツールを利用しましょう。

## 4. トレーシング サンプルの実行

リポジトリのルートまたは仮想環境を有効化したシェルで以下を実行します。

```bash
APPLICATIONINSIGHTS_CONNECTION_STRING="<your-connection-string>" \
ENABLE_AGENT_TRACE_CONTENT=true \
python -m samples.python.06_observability_tracing.main
```

想定されるコンソール出力:

- `Application Insights exporter configured for tracing output`
- `DefaultAzureCredential acquired a token ...`
- `Agent run did not complete successfully (status=RunStatus.FAILED, error={'code': 'server_error', ...})`
- `Cleaning up created agent`

上記のように `server_error` により終了コード 1 となる場合があります。これでもトレース パイプラインは動作しており、演習上問題はありません。

## 5. 実行例 (ラン ID とテレメトリ件数)

最新のワークショップ実行では次のメタデータが得られました (日本時間)。

| 実行 | 開始時刻 | スレッド ID | ラン ID | 結果 | 受信件数 |
| --- | --- | --- | --- | --- | --- |
| 1 | 12:20 | `thread_avklT9py2T0fwePYn0GI7zGW` | `run_Py3LqbJQBQReVqf0zHHjOFto` | `FAILED` (`server_error`) | 14 |
| 2 | 12:25 | `thread_9VDUdO3JBvp74h4IO8UGRTk9` | `run_FQ8Wk8JyppdBDO3vzNieeenx` | `FAILED` (`server_error`) | 13, 7, 9, 12 |

実際の値は毎回異なります。コンソール出力からご自身のラン ID を記録しておきましょう。

## 6. Application Insights でトレースを確認

1. 接続文字列に対応する Application Insights リソースを開きます。
2. **Logs (Analytics)** を選択し、ラン ID で絞り込む Kusto クエリを実行します。

    ```kusto
    traces
    | where customDimensions["gen_ai.thread.run.id"] == "run_FQ8Wk8JyppdBDO3vzNieeenx"
    | order by timestamp asc
    | project timestamp, message, severityLevel, customDimensions
    ```

3. サンプルから送信された全てのエージェント関連トレースを確認する場合は、サービス メタデータでフィルターします。

    ```kusto
    traces
    | where customDimensions["gen_ai.system"] == "az.ai.agents"
    | where customDimensions["service.name"] == "workshop-agent-tracing"
    | summarize count() by bin(timestamp, 5m), customDimensions["gen_ai.event"]
    ```

4. `ENABLE_AGENT_TRACE_CONTENT=true` の場合、`customDimensions.gen_ai.event.content` にメッセージやツールの詳細が格納されます。

## 7. トラブルシューティング

| 症状 | 対処方法 |
| --- | --- |
| `ModuleNotFoundError: No module named 'azure.monitor'` | `pip install -r requirements.txt` が完了しているか確認してください。エクスポーターは依存関係に含まれています。 |
| `Failed to load configuration: ... PROJECT_ENDPOINT` | 環境変数が正しく設定されているか、`samples/python/common/config.py` で読み込めているか確認します。 |
| `Agent run did not complete successfully (server_error)` | 時間をおいて再試行するか、Azure AI Foundry 側の状態やクォータを確認します。トレースは送信されています。 |
| Application Insights にデータが表示されない | 接続文字列が正しいリソースを指しているか確認し、クエリで指定したラン/スレッド ID が一致しているか見直してください。 |

## 8. 後片付け

- 各実行で作成した一時エージェントは自動削除されるため、ポータルでの手動削除は不要です。
- 作業終了後は仮想環境を `deactivate` で無効化します。
- 接続文字列などの秘密情報を含む一時ファイルは削除してください。

## 9. 参考資料

- [Azure AI Foundry Agents クイックスタート (Python)](https://learn.microsoft.com/ja-jp/azure/ai-foundry/agents/quickstart?pivots=programming-language-python-azure)
- [Azure Monitor OpenTelemetry エクスポーター (Python)](https://learn.microsoft.com/ja-jp/azure/azure-monitor/app/opentelemetry-configuration)
- [OpenTelemetry Python ドキュメント](https://opentelemetry.io/docs/languages/python/)
- 内部レポート: [`observability_tracing_report.md`](../observability_tracing_report.md)
