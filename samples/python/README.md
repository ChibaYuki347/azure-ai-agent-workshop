# Python サンプル集：Azure AI Foundry Agent Service ワークショップ

Azure AI Foundry Agent Service を扱うワークショップの各セッションに対応した Python サンプルコードです。公式ドキュメントのベストプラクティスに沿っており、[Quickstart: Create a new agent (Python)](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstart?pivots=programming-language-python-azure)、[Azure AI Search tool](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/azure-ai-search?pivots=programming-language-python)、[Logic Apps integration](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/logic-apps?pivots=programming-language-python) などの手順を参考にしています。

## フォルダー構成

| ディレクトリ | 対応セッション | 説明 |
| --- | --- | --- |
| `01_minimal_agent/` | Day1 S9 | 最小構成のエージェントと Code Interpreter ツールの利用サンプル。 |
| `02_ai_search_rag/` | Day1 S13–S17 | Azure AI Search tool を使った RAG ワークフロー。引用の取り扱い例を含みます。 |
| `03_logic_app_tool/` | Day1 S18–S20 | Logic Apps を Function Tool として連携し、通知メールを送信するサンプル。 |
| `04_connected_agents/` | Day1 S21–S24 & Day2 S25–S27 | Typer/Rich ベースの CLI から Connected Agents ワークフローをオーケストレーション。 |
| `05_evaluation/` | Day2 S28–S31 | Azure AI Evaluation SDK を利用した Intent Resolution / Content Safety の評価。 |
| `common/` | 共通 | 共有ユーティリティ (設定、ロギング、Logic App ラッパーなど)。 |

## 前提条件

1. Azure サブスクリプションと Azure AI Foundry プロジェクト。
2. モデル デプロイ (例: `gpt-4o-mini`) が `Models + Endpoints` に存在すること。[ドキュメント](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstart#configure-and-run-an-agent) を参照。
3. Azure CLI で `az login` 済みであること。
4. Python 3.10 以上。

## セットアップ

```bash
cd samples/python
python -m venv .venv
source .venv/bin/activate  # Windows の場合は .venv\Scripts\activate
pip install -r requirements.txt
```

## 共通環境変数

以下は全サンプル共通で必要です。`.env` 等に設定し、`source` で読み込むかシェル上でエクスポートしてください。

| 変数名 | 必須 | 説明 |
| --- | --- | --- |
| `PROJECT_ENDPOINT` | ◯ | Azure AI Foundry プロジェクトのエンドポイント (`https://<resource>.services.ai.azure.com/api/projects/<project>`) |
| `MODEL_DEPLOYMENT_NAME` | ◯ | 使用するモデル デプロイ名 |

## シナリオ別の追加設定

| サンプル | 追加で必要な変数 | 補足 |
| --- | --- | --- |
| `02_ai_search_rag` | `AI_SEARCH_CONNECTION_ID`, `AI_SEARCH_INDEX_NAME` | [Azure AI Search tool の接続手順](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/azure-ai-search#setup)。接続はプロジェクトの Management Center で事前に作成します。 |
| `03_logic_app_tool` | `LOGIC_APP_CALLBACK_URL` | Logic Apps (HTTP トリガー) のコールバック URL。消費プランでのワークフローに対応しています。参考: [Logic Apps 連携ガイド](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/logic-apps?pivots=programming-language-python)。 |
| `04_connected_agents` | `WORKSHOP_RESEARCH_AGENT_ID`, `WORKSHOP_ANALYSIS_AGENT_ID`, `WORKSHOP_WRITING_AGENT_ID` (任意) | Foundry 上で事前に作成した Connected Agent の ID。省略時は `research-agent` / `analysis-agent` / `writing-agent` を使用します。 |
| `05_evaluation` | `EVAL_AOAI_ENDPOINT`, `EVAL_AOAI_DEPLOYMENT`, `EVAL_AOAI_API_KEY`, `EVAL_AOAI_API_VERSION` (省略可), `AZURE_AI_PROJECT` (任意) | 評価用の Azure OpenAI モデルへのアクセス情報。`AZURE_AI_PROJECT` を指定すると Content Safety 評価結果が Foundry プロジェクトに保存されます。参考: [Evaluate your AI agents locally](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/agent-evaluate-sdk)。 |

## 実行例

```bash
python -m samples.python.01_minimal_agent.main
python -m samples.python.02_ai_search_rag.main
python -m samples.python.03_logic_app_tool.main
python -m samples.python.04_connected_agents.main run
python -m samples.python.05_evaluation.main
```

`04_connected_agents` は [Typer](https://typer.tiangolo.com/) を利用した CLI です。利用可能なサブコマンドは `--help` で確認できます。

```bash
python -m samples.python.04_connected_agents.main --help
python -m samples.python.04_connected_agents.main info
python -m samples.python.04_connected_agents.main run --topic "AI impact on supply chains"
```

各スクリプトは終了時に作成したエージェントを削除するよう実装されており、ワークショップ後にポータル上で手動削除する必要はありません。

## 注意事項

- 公式 SDK の最新バージョンを使用してください。`requirements.txt` のバージョンは 2025 年 9 月時点の推奨値です。
- 認証には `DefaultAzureCredential` を利用しており、Managed Identity / Visual Studio Code サインインなど標準フローをサポートします。
- Logic Apps 連携サンプルでは HTTP トリガーを想定しています。セキュリティ要件に応じて Azure AD 認証や専用接続に置き換えてください。
- 評価サンプルはプレビュー機能を利用します。商用利用時は最新のプレビュー条件を確認してください。

