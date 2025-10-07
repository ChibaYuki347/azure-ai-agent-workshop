# Workshop構成案：Azure AI Foundry Agent Service入門（全2日）

---

## Day 1（23日）—「Agentを“作って動かす”」13:00–17:00

### モジュールA：導入（概念 & 全体像）

**S1. オープニング & ゴール**

* **入れる要素**：ゴール3点（①Agentic AIの基本要素 ②最小Agentの構築 ③RAG+ツール実行の体験）／全体アジェンダ図
* **Notes**：本ワークショップで扱う“Azure AI Foundry Agent Service（以降「Agent Service」）”は、モデル・ツール・観測性・ID・ネットワークを束ねる実行基盤であることを強調。([Microsoft Learn][1])

**S2. Agentic AIとは（Copilot/Assistantsとの違い）**

* **入れる要素**：比較表（アシスタント≒対話中心 vs Agent≒目標達成＋ツール実行＋状態管理）
* **Notes**：Agent Serviceは**スレッド管理**・**ツール呼び出し**・**コンテンツセーフティ**・**ID/ネットワーク/可観測性統合**を提供。([Microsoft Learn][1])

**S3. Azureの選択肢と位置づけ**

* **入れる要素**：3カラム図（Agent Service GA／Assistants API（Preview）／フレームワーク：Semantic Kernel）
* **Notes**：Assistantsはプレビューで、Agent Serviceは運用要件（観測性・ネットワーク等）を標準で備える点を対比。([Microsoft Learn][2])

---

### モジュールB：Agent Serviceの基礎

**S4. Agent Service一枚絵（アーキテクチャ）**

* **入れる要素**：Portal/REST/SDK、モデル、Tools（Logic Apps等）、RAG（AI Search）、Observability、Entra ID、Private Linkの関係図
* **Notes**：単一ランタイムでこれらを統合。用語（Agent/Thread/Message/Run/Tool）を明確化。([Microsoft Learn][1])

**S5. 管理される“状態”**

* **入れる要素**：データ保持の図（Threads / Messages / Runs / Files）
* **Notes**：Agent Serviceは**ステートフルAPI**。スレッド等のエンティティとファイルを保持することを明示。([Microsoft Learn][3])

**S6. ツールの種類と追加方法**

* **入れる要素**：内蔵ツール一覧（Bing Grounding, Azure AI Search, Logic Apps, サードパーティ等）＆ツール追加UIのスクリーンショット（差し替え用プレースホルダ）
* **Notes**：ツールの役割と追加手順の概観。([Microsoft Learn][4])

**S7. クイックスタート（作成→会話→実行）**

* **入れる要素**：Portal手順 or REST/SDKの最小ステップ（図＋簡単な擬似コード）
* **Notes**：最小Agent作成～スレッド作成～メッセージ追加～run実行の流れ。([Microsoft Learn][5])

---

### モジュールC：ハンズオン①「Hello, Agent」

**S8. デモ計画（成功基準・ロールバック）**

* **入れる要素**：成功条件（ユーザ質問→Agent応答）／失敗時の切替（モデル/デプロイ名）
* **Notes**：Portal/SDKいずれでもOK、認証は`DefaultAzureCredential`推奨と説明。

**S9. SDK最小コード（Python）**

* **入れる要素**：**Agent作成→Thread→Message→Run** の10–15行サンプル
* **Notes**：コードは“概念理解用”。本番は例外処理・リトライ・ロギング必須と補足。([Microsoft Learn][5])

**S10. よくあるつまずき（モデル名・権限・リージョン）**

* **入れる要素**：チェックリスト（デプロイ名一致／RBAC／クォータ確認）
* **Notes**：RBAC/Quotaは後半で深掘りする旨を案内。([Microsoft Learn][6])

**S11. スレッドとメッセージの設計Tips**

* **入れる要素**：短期/長期スレッド、会話スコープと永続化の図
* **Notes**：スレッドは“会話と状態の最小単位”。FAQの“保存対象”と絡めて説明。([Microsoft Learn][3])

**S12. 練習課題**

* **入れる要素**：プロンプト指示の工夫（スタイル／根拠要求／手順化）
* **Notes**：後の評価モジュールで Azure AI Evaluation の Agent evaluators（Task Adherence / Tool Call Accuracy など）で成果を測定する前振り。([Microsoft Learn][16])

---

### モジュールD：RAG（Azure AI Search Tool）で根拠付け

**S13. なぜRAGか（ハルシ対策と最新性）**

* **入れる要素**：生成のみ vs 検索＋生成の比較図
* **Notes**：Agent Serviceに**Azure AI Search tool**を接続して回答を強化できる。([Microsoft Learn][7])

**S14. 接続手順（Connections→Add→AI Search）**

* **入れる要素**：Portal手順（Connectionsタブ→Azure AI Search）／CLI/SDK例の断片
* **Notes**：接続はプロジェクト単位。インデックス設計は後述のチューニングへ。([Microsoft Learn][7])

**S15. 検索モードの選択（Keyword/Semantic/Vector/Hybrid）**

* **入れる要素**：適用条件の表（例：FAQ＝Semantic、技術文書＝Hybrid）
* **Notes**：**Agentic Retrieval**のリファレンスも提示。([Microsoft Learn][8])

**S16. デモ：社内ドキュメントRAG**

* **入れる要素**：クエリ→ヒット→引用抽出（出典URL/タイトル）フロー図
* **Notes**：回答の**引用**（ソース提示）を出力に含めるプロンプト例を紹介。

**S17. チューニング（埋め込み・フィールド設計・キャッシュ）**

* **入れる要素**：インデックス設計のチェックリスト
* **Notes**：“Agent to Agent + Search”パターンのセットアップガイドを参照にしつつ、Azure AI Evaluation の RAG evaluators（Groundedness / Response Completeness / Retrieval）で効果検証。([Microsoft Learn][8], [Microsoft Learn][15])

---

### モジュールE：ツール実行（アクション化）

**S18. Logic Apps連携（1,400+コネクタ）**

* **入れる要素**：チケット起票や承認フローなどの**業務アクション**例
* **Notes**：Agentから**Logic Apps**等のツールを呼び出し可能（カタログの訴求点）。([Microsoft Azure][9])

**S19. OpenAPI/Functionsツール化の設計ポイント**

* **入れる要素**：関数呼び出し（Function Calling）前提のI/O設計／入力バリデーション
* **Notes**：ツールは“最小で安全”に。失敗時のフォールバック手順を設ける。([Microsoft Learn][4])

**S20. デモ：Logic Appsで外部SaaSを操作**

* **入れる要素**：フロー図（Agent→Tool→SaaS）／監査ログの確認ポイント
* **Notes**：“誰が何を実行したか”を後日の観測モジュールで可視化予定。

---

### モジュールF：Connected Agents（マルチエージェント入門）

**S21. パターン紹介**

* **入れる要素**：オーケストレーター＋サブエージェント（調査／要約／検証／生成）の関係図
* **Notes**：**Connected Agents**として、AgentからAgentへの委譲を設定できる。([Microsoft Learn][10])

**S22. 役割分担とプロンプト設計**

* **入れる要素**：責務分離のテンプテート（例：Critic/Planner/Executor）
* **Notes**：“どのAgentがどのツールを持つか”を明確に。

**S23. 小デモ or ワーク**

* **入れる要素**：リサーチ→要約→検証→レポート生成の3分デモ
* **Notes**：Day2で評価・監視・運用に接続。

**S24. Day1 まとめ & 質疑**

* **入れる要素**：本日の成果物／明日の予告（評価・監視・セキュリティ・レート制御）
* **Notes**：次回までの宿題（RAG用データの準備など）を提示。

---

## Day 2（30日）—「Agentを“評価し、守り、運用する”」13:00–17:00

### Day2 モジュール クイックリファレンス

| モジュール | 目的 | 主なトピック / ハンズオン | 成果物・次モジュール連携 |
| --- | --- | --- | --- |
| G マルチエージェント深掘り | マルチエージェント運用の設計判断軸を整理し、Connected Agentsを活用する準備を整える。 | 代表パターン比較、SLO指標設計、委譲設計の観点共有。 | S26でのKPI設計資料、S27ハンズオン用の役割分担メモ。 |
| H Evaluation（Azure AI Evaluation） | 品質・安全性・エージェント指標を体系的に評価し、改善ループを定着させる。 | UI/SDK/クラウド評価の流れ、RAG評価デモ、手動レビューとA/B比較。 | 改善チケット、Observabilityで追跡する指標のしきい値。 |
| I Observability（運用可視化） | 運用時のKPIとアラート設計を明確化し、評価結果と連携したモニタリング基盤を構築。 | App Insights統合、有効化手順、ダッシュボードとアラート設計。 | 運用ダッシュボード、SLOアラート設定、Securityチームへの共有資料。 |
| J Responsible AI（Content Safety） | コンテンツ安全性ガードレールを理解し、評価と監視の結果を踏まえた運用判断を定義。 | カテゴリ別閾値設定、ガードレール配置、ハンズオンによる逸脱検証。 | 安全性ポリシー、インシデント対応フローのドラフト。 |
| K アイデンティティ & 権限 | 最小権限設計と監査性を確保し、Day1で構築したAgentの運用ガバナンスを固める。 | RBAC整理、Agent IDの管理、認証パターン比較。 | 役割ごとのアクセス表、ID管理計画。 |
| L ネットワーク隔離 | ハイブリッド/企業ネットワーク要件に合わせた接続モデルを整理。 | Managed Network/Private Link/VNet活用の比較と構成手順。 | ネットワーク設計図、セキュリティレビュー用チェックリスト。 |
| M クォータ・レート制御・コスト | モデル利用の制御と最適化方針を定め、安定運用とコスト管理を両立。 | Quota/RPM設計、APIMでのスロットリング、コスト抑制Tips。 | レート制御ポリシー、コスト試算シート。 |
| N クロージング | 本番投入に向けたチェックと次のステップを明確化。 | 本番チェックリストレビュー、参考リソース紹介。 | 運用ロードマップ、学習・展開プラン。 |

### モジュールG：マルチエージェント深掘り

**S25. 代表パターン（Sequential/Parallel/Critic-Loop）**

* **入れる要素**：3パターン図と失敗例（無限ループ／冗長ツール呼び出し）
* **Notes**：プランニングはSemantic Kernel等のフレームワーク併用も選択肢。([Microsoft Learn][11])

**S26. 責務・SLO設計**

* **入れる要素**：Agent別KPI（成功率、Tool Call成功率、遅延）
* **Notes**：SLOは後述のObservabilityで計測・可視化し、Azure AI Evaluation の Agent evaluators（Intent Resolution / Tool Call Accuracy / Task Adherence）のスコアをKPIに活用。([Microsoft Learn][12], [Microsoft Learn][16])

**S27. ハンズオン：Connected Agentsの構成**

* **入れる要素**：Portal操作の要点スクリーン（Add Connected Agent）
* **Notes**：委譲先の説明文（境界条件・入力/出力契約）を具体に書く。([Microsoft Learn][10])

---

### モジュールH：Evaluation（Azure AI Evaluation）

#### S28. なぜ評価が必要か（改訂）

* **入れる要素**：Quality（Relevance / Coherence / Fluency / Similarity）、RAG特有（Groundedness / Response Completeness / Retrieval）、Safety（Violence / Sexual / Self-harm / Hate など）、Agent特有（Intent Resolution / Tool Call Accuracy / Task Adherence）の指標カテゴリ。
* **Notes**：Azure AI Evaluation がこれらの指標を標準で提供し、評価結果をプロジェクトに記録して継続改善に役立つ点を強調。([Microsoft Learn][13], [Microsoft Learn][15], [Microsoft Learn][16])

#### S29. 評価の作り方（UI / SDK / クラウド）

* **入れる要素**：UIウィザードでデータセット・評価対象・メトリクスを指定→ラン比較、SDK（ローカル）で`azure-ai-evaluation`の`evaluate()`を呼び出す手順、クラウド評価（Preview）でチーム共有できる評価記録を作成する流れ。
* **Notes**：UI/SDK/クラウドの使い分け（規模・自動化・共同作業）を整理し、評価結果はAzure AIプロジェクトで一元管理できることを伝える。([Microsoft Learn][13], [Microsoft Learn][14], [Microsoft Learn][15])

#### S30. デモ：RAG回答の評価（改訂）

* **入れる要素**：質問・期待回答・コンテキストを含むデータセットに対し、Groundedness / Response Completeness / Retrieval を選択して実行し、パス/フェイルと理由文を確認するフロー。
* **Notes**：評価結果から改善アクション（プロンプト更新／ツール設定／索引チューニング）へつなげるサイクルを示す。([Microsoft Learn][15])

#### S31. 手動評価とA/B比較のヒント（改訂）

* **入れる要素**：ポータルのEvaluationページでのしきい値設定、サンプル詳細のレビュー、ラン比較UIによるA/B評価の手順。
* **Notes**：自動評価に手動レビューを組み合わせ、意思決定の裏付けとしてラン比較ダッシュボードを活用する。([Microsoft Learn][13])

---

### モジュールI：Observability（運用可視化）

**S32. 何を観測するか（Ops/Quality/Safety）**

* **入れる要素**：KPIマップ（遅延・リク数・トークン・安全性ブロック率）
* **Notes**：**Azure AI Foundry Observability**は**Application Insights**と統合。([Microsoft Learn][12])

**S33. セットアップの流れ**

* **入れる要素**：プロジェクト→Observability有効化→App Insights接続のフロー図
* **Notes**：監視は“継続運用の前提”。Azure AI Evaluation の結果はプロジェクトに記録され、ポータルでラン比較や詳細ドリルダウンが可能。([Microsoft Learn][12], [Microsoft Learn][13])

**S34. ダッシュボード例（アラート/診断）**

* **入れる要素**：異常検知（急増/急減）・SLO逸脱の例
* **Notes**：品質＆安全性の同時モニタリングを推奨。([TECHCOMMUNITY.MICROSOFT.COM][17])

**S35. 拡張（サードパーティ/OTel連携の検討）**

* **入れる要素**：OpenTelemetry系の参考（任意）
* **Notes**：公式以外の選択肢もある旨の参考。([Dynatrace][18])
* **Handout**：実機演習では [Observability Tracing Hands-on Guide (EN)](../observability-tracing-handson.md) / [オブザーバビリティ トレーシング ハンズオン ガイド (JA)](observability-tracing-handson.md) を配布し、Application Insights 連携ステップを補足。

---

### モジュールJ：Responsible AI（Content Safety）

**S36. Content Safetyの基本**

* **入れる要素**：4カテゴリ（Hate/Violence/Sexual/Self-harm）＋閾値調整の図
* **Notes**：ポリシーと閾値は**ユースケースに応じて検証**が必要。([Microsoft Learn][19], [Microsoft Azure][20])

**S37. エージェントへの適用ポイント**

* **入れる要素**：入力・中間出力・最終出力でのガードレール配置図
* **Notes**：検出→ブロック/再生成/赤チーム評価の流れ。

**S38. ラボ：不適切入力の検出テスト**

* **入れる要素**：“Try it”でのテスト手順（スクショ差替え）
* **Notes**：安全性ログの観測と逸脱時の対応を解説。([Microsoft Learn][19])

---

### モジュールK：アイデンティティ & 権限（Admin）

**S39. RBACと役割設計**

* **入れる要素**：プロジェクト/ハブに対するAzure RBAC（ビルトイン＋カスタム役割）表
* **Notes**：最小権限で分離（Dev/Reviewer/Operator等）。([Microsoft Learn][6])

**S40. Agent IDの考え方（非人間IDの管理）**

* **入れる要素**：Agent IDとDefender/Purview連携の図（監査・統制の観点）
* **Notes**：“デジタルレイバー”の統制強化トレンドを共有。([TECHCOMMUNITY.MICROSOFT.COM][21])

**S41. 認証（Keyless/Entra ID）**

* **入れる要素**：Managed Identity/トークン/キーの比較表と推奨
* **Notes**：Azure AI/Agent/On Your Dataでの認証オプション整理。([Microsoft Learn][22])

---

### モジュールL：ネットワーク隔離（Admin）

**S42. 選択肢の全体像**

* **入れる要素**：Hub/Projectの**Managed Network**と**Private Link**、Agent Serviceの**VNet利用（注：SKU/方式差異）**を対比する図
* **Notes**：ハブ側は**Managed VNet**が基本。Agent ServiceのVNet対応（Network Injection/BYO VNet）の最新動向は公式/TechCommunityを併読。([Microsoft Learn][23], [TECHCOMMUNITY.MICROSOFT.COM][24])

**S43. AgentのVNet化（ハウツーの要点）**

* **入れる要素**：Agent ServiceでのVNet利用ハイレベル手順（サブネット委任・アウトバウンド制御）
* **Notes**：専用VNetでエージェントの出入口を制御。([Microsoft Learn][25])

**S44. Azure OpenAIのネットワーク保護**

* **入れる要素**：OpenAIリソースPrivate Endpoint構成の参照アーキ図
* **Notes**：Agent→OpenAI間もプライベート経路化。([Microsoft Learn][26])

**S45. On Your Dataのネットワーク/アクセス**

* **入れる要素**：データソースへの認証（MI/トークン等）とネットワーク到達性の整理
* **Notes**：データ到達と認証の両輪で設計。([Microsoft Learn][27])

---

### モジュールM：クォータ・レート制御・コスト

**S46. Quota/Rateの基礎（TPM/RPM/Capacity）**

* **入れる要素**：TPM/RPMの関係、モデル別傾向、**単位容量**の考え方
* **Notes**：モデルによりRPM:TPM比が異なる点を強調。最新の**Azure OpenAI Quotas/Limits**を必ず参照。([Microsoft Learn][28])

**S47. デプロイ配賦（TPM割当）**

* **入れる要素**：PortalでのTPM割当のスクリーン（差替え）
* **Notes**：サブスクリプション×リージョン×モデル単位の配賦を設計。([Microsoft Learn][29])

**S48. APIMでの**Token Rate Limit**適用**

* **入れる要素**：`azure-openai-token-limit-policy`の適用例（要点だけの抜粋）
* **Notes**：**1顧客＝1キー**等で“使い過ぎ”を抑止できる。([Microsoft Learn][30])

**S49. APIMその他のスロットリング/プラン制御**

* **入れる要素**：`rate-limit-by-key`や**クォータ**（月次等）との併用パターン
* **Notes**：組織側ガードレールとして有効。([Microsoft Learn][31])

**S50. コスト最適化チェックリスト**

* **入れる要素**：キャッシュ（過去応答/要約）・RAGのドキュメント粒度・レスポンス制御（出力長）・モデル選定（mini系の活用）
* **Notes**：評価→監視→調整の継続運用を前提に。

---

### モジュールN：クロージング

**S51. 本番投入チェックリスト**

* **入れる要素**：安全性（Content Safety/赤チーム）／運用（Observability/SLO）／ID&ネットワーク／レート／BCP
* **Notes**：自社要件へ転記できる形で配布。関連公式ハブも再掲。([Microsoft Learn][32])

**S52. 次の一歩 & 参考リソース**

* **入れる要素**：チュートリアル、サンプル、学習パスのリンク集
* **Notes**：最新情報はLearn/Docs/TechCommunityを追う運用に。([Microsoft Learn][5], [TECHCOMMUNITY.MICROSOFT.COM][21])

---

## Day2 デモ用サンプルコード集（Python / .NET）

ワークショップ Day2（評価・監視・安全性・運用）の各モジュールに直結する最小サンプルです。以下を上から順に設定・実行すると、S25〜S50のデモにそのまま活用できます。

### 0) 事前準備（共通）

```bash
# Azure AI Foundry Project
export PROJECT_ENDPOINT="https://<xxx>.services.ai.azure.com/api/projects/<project-name>"
export MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>"

# Application Insights / Log Analytics
export APPLICATIONINSIGHTS_CONNECTION_STRING="<App Insights の接続文字列>"
export LOGS_WORKSPACE_ID="<Log Analytics Workspace ID>"

# Azure AI Content Safety
export CONTENT_SAFETY_ENDPOINT="https://<your-contentsafety>.cognitiveservices.azure.com"
export CONTENT_SAFETY_KEY="<content-safety-key>"

# (任意) APIM 経由のレート制御デモ用
export APIM_OPENAI_BASE="https://<your-apim>.azure-api.net"
export APIM_SUBSCRIPTION_KEY="<your-apim-subscription-key>"
export OPENAI_DEPLOYMENT="<your-aoai-deployment>"
export OPENAI_API_VERSION="2024-06-01"
```

> Agent/Thread/Run の語彙や最小ステップは概要・クイックスタートを参照。([Microsoft Learn][1], [Microsoft Learn][5])

### 1) 【G】Connected Agents（マルチエージェント）

#### Python

```python
# pip install azure-ai-projects azure-ai-agents azure-identity
import os
from azure.ai.agents.models import ConnectedAgentTool, MessageRole
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

stock_agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="stock_price_bot",
    instructions=(
        "You get the stock price of a company. If real-time is not available, "
        "return the last known price."
    ),
)

connected = ConnectedAgentTool(
    id=stock_agent.id,
    name=stock_agent.name,
    description="Gets the stock price of a company",
)

main_agent = project.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="research_agent",
    instructions="Use available tools to answer questions.",
    tools=connected.definitions,
)

thread = project.agents.threads.create()
project.agents.messages.create(
    thread_id=thread.id,
    role=MessageRole.USER,
    content="What is the stock price of Microsoft?",
)
run = project.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=main_agent.id,
)

for message in project.agents.messages.list(thread_id=thread.id).text_messages:
    print(message)
```

#### .NET (C#)

```csharp
// dotnet add package Azure.AI.Agents.Persistent --prerelease
// dotnet add package Azure.Identity
using Azure.AI.Agents.Persistent;
using Azure.Identity;

var endpoint = Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var model = Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");

var client = new PersistentAgentsClient(endpoint, new DefaultAzureCredential());

var stockAgent = client.Administration.CreateAgent(
    model: model,
    name: "stock_price_bot",
    instructions: "Get stock prices. If real-time isn't available, return the last known price."
);

var connected = new ConnectedAgentToolDefinition(
    new ConnectedAgentDetails(
        stockAgent.Id,
        stockAgent.Name,
        "Gets the stock price of a company"
    )
);

var mainAgent = client.Administration.CreateAgent(
    model: model,
    name: "research_agent",
    instructions: "Use available tools to answer questions.",
    tools: [connected]
);

var thread = client.Threads.CreateThread();
client.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "What is the stock price of Microsoft?"
);
var run = client.Runs.CreateRun(thread, mainAgent);

while (run.Status is RunStatus.InProgress or RunStatus.Queued)
{
    Thread.Sleep(500);
    run = client.Runs.GetRun(thread.Id, run.Id);
}

foreach (var message in client.Messages.GetMessages(thread.Id, order: ListSortOrder.Ascending))
{
    foreach (var content in message.ContentItems)
    {
        if (content is MessageTextContent text)
        {
            Console.WriteLine($"{message.Role}: {text.Text}");
        }
    }
}
```

> Connected Agents の設定や委譲パターンは公式 How-to を参照。([Microsoft Learn][10])

### 2) 【H】Evaluation（品質・安全性・エージェント指標）

#### 2-A. Python：Continuous Evaluation（クラウド）

```python
# pip install azure-ai-projects azure-identity azure-monitor-query
import os
from datetime import timedelta
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentEvaluationRequest, EvaluatorIds
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus

project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

evaluators = {
    "Relevance": {"Id": EvaluatorIds.Relevance.value},
    "Fluency": {"Id": EvaluatorIds.Fluency.value},
    "Coherence": {"Id": EvaluatorIds.Coherence.value},
    "ToolCallAccuracy": {"Id": EvaluatorIds.ToolCallAccuracy.value},
}

app_insights_cs = project.telemetry.get_application_insights_connection_string()

eval_run = project.evaluation.create_agent_evaluation(
    AgentEvaluationRequest(
        thread=thread.id,
        run=run.id,
        evaluators=evaluators,
        app_insights_connection_string=app_insights_cs,
    )
)
print("Evaluation requested:", eval_run.name)

logs = LogsQueryClient(DefaultAzureCredential())
kql = f"""
traces
| where message == "gen_ai.evaluation.result"
| where customDimensions["gen_ai.thread.run.id"] == "{run.id}"
"""
response = logs.query_workspace(
    os.environ["LOGS_WORKSPACE_ID"],
    kql,
    timespan=timedelta(days=1),
)

if response.status == LogsQueryStatus.SUCCESS:
    for table in response.tables:
        for row in table.rows:
            print(dict(zip(table.columns, row)))
```

> Continuous Evaluation と App Insights 連携は公式ガイドを参照。([Microsoft Learn][34])

#### 2-B. Python：ローカル評価 SDK（RAG 指標など）

```python
# pip install azure-ai-evaluation
from azure.ai.evaluation import evaluate

result = evaluate(
    data="dataset.jsonl",
    evaluators={
        "Groundedness": "groundedness",
        "ResponseCompleteness": "response_completeness",
        "Retrieval": "retrieval",
    },
    evaluation_name="rag-eval-run",
)

print(result["metrics"])
```

> 組み込み評価器の一覧と活用は Evaluation SDK を参照。([Microsoft Learn][36])

#### 2-C. .NET：クラウド評価 API

```csharp
// dotnet add package Azure.AI.Projects --prerelease
// dotnet add package Azure.Identity
using Azure.AI.Projects;
using Azure.Identity;

var projects = new AIProjectsClient(endpoint, new DefaultAzureCredential());

var evaluators = new Dictionary<string, EvaluatorConfiguration>
{
    { "Relevance", new EvaluatorConfiguration(EvaluatorIds.Relevance) },
    { "Fluency", new EvaluatorConfiguration(EvaluatorIds.Fluency) },
    { "ToolCallAccuracy", new EvaluatorConfiguration(EvaluatorIds.ToolCallAccuracy) },
};

var request = AzureAIProjectsModelFactory.AgentEvaluationRequest(
    runId: run.Id,
    threadId: thread.Id,
    evaluators: evaluators
);

var evaluation = projects.Evaluations.CreateAgentEvaluation(request);
Console.WriteLine($"Agent evaluation started: {evaluation.Value.Name}");
```

> .NET SDK の `Evaluations.CreateAgentEvaluation` を活用。([Microsoft Learn][37])

### 3) 【I】Observability（監視・トレース）

#### 3-A. Python：OpenTelemetry で App Insights 送信

```python
# pip install azure-monitor-opentelemetry opentelemetry-sdk
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
)

# 以降に AIProjectClient を利用してエージェントを実行すると、トレースが App Insights に送信される
```

> OpenTelemetry の設定は Azure Monitor ガイドを参照。([Microsoft Learn][38])

> 🔧 実装例: `samples/python/06_observability_tracing/main.py` では `AIAgentsInstrumentor` と OpenTelemetry エクスポーターを組み合わせ、任意でメッセージ内容のトレースも有効化するハンズオン用コードを提供しています。

#### 3-B. .NET：App Insights ログを KQL で取得

```csharp
// dotnet add package Azure.Monitor.Query
// dotnet add package Azure.Identity
using Azure.Identity;
using Azure.Monitor.Query;

var logsClient = new LogsQueryClient(new DefaultAzureCredential());

var query = $@"
traces
| where message == "gen_ai.evaluation.result"
| where tostring(customDimensions["gen_ai.thread.run.id"]) == "{run.Id}"
";

var result = logsClient.QueryWorkspace(
    Environment.GetEnvironmentVariable("LOGS_WORKSPACE_ID"),
    query,
    TimeSpan.FromDays(1)
);

foreach (var table in result.Value.Tables)
{
    foreach (var row in table.Rows)
    {
        Console.WriteLine(string.Join(" | ", row));
    }
}
```

> Logs Query SDK の利用例は公式サンプルを参照。([Microsoft Learn][39])

### 4) 【J】Responsible AI（Content Safety）

#### Python：入出力の安全性チェック

```python
# pip install azure-ai-contentsafety
import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    AnalyzeTextOutputType,
    TextCategory,
)
from azure.core.credentials import AzureKeyCredential

client = ContentSafetyClient(
    endpoint=os.environ["CONTENT_SAFETY_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["CONTENT_SAFETY_KEY"]),
)

def is_safe_text(text: str) -> bool:
    options = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
        output_type=AnalyzeTextOutputType.FOUR_SEVERITY_LEVELS,
    )
    result = client.analyze_text(options)
    severities = [category.severity for category in result.categories_analysis]
    return max(severities, default=0) < 4

user_input = "..."
if not is_safe_text(user_input):
    raise ValueError("Input rejected by safety policy")

agent_output = "..."
if not is_safe_text(agent_output):
    agent_output = "The response was withheld due to safety policy."
```

> Content Safety SDK の判定ロジック詳細は README を参照。([Microsoft Learn][40])

#### .NET：入出力の安全性チェック

```csharp
// dotnet add package Azure.AI.ContentSafety
// dotnet add package Azure.Identity
using Azure;
using Azure.AI.ContentSafety;

var csClient = new ContentSafetyClient(
    new Uri(Environment.GetEnvironmentVariable("CONTENT_SAFETY_ENDPOINT")),
    new AzureKeyCredential(Environment.GetEnvironmentVariable("CONTENT_SAFETY_KEY"))
);

bool IsSafe(string text)
{
    var options = new AnalyzeTextOptions(text)
    {
        OutputType = AnalyzeTextOutputType.FourSeverityLevels,
    };

    var response = csClient.AnalyzeText(options);
    var maxSeverity = response.Value.CategoriesAnalysis.Max(category => (int)category.Severity);
    return maxSeverity < 4;
}
```

> .NET 版 Content Safety SDK の詳細は公式ドキュメントを参照。([Microsoft Learn][41])

### 5) 【M】レート制御・コスト最適化（APIM + 429 リトライ）

APIM 側で `azure-openai-token-limit-policy` を適用し、`tokens-per-minute` や `counter-key` を設定します。([Microsoft Learn][30])

#### Python：429 / Retry-After を尊重したリトライ

```python
# pip install requests
import os
import time
import requests

def call_openai_via_apim(messages):
    url = (
        f"{os.environ['APIM_OPENAI_BASE']}/openai/deployments/"
        f"{os.environ['OPENAI_DEPLOYMENT']}/chat/completions"
        f"?api-version={os.environ['OPENAI_API_VERSION']}"
    )
    headers = {
        "Ocp-Apim-Subscription-Key": os.environ["APIM_SUBSCRIPTION_KEY"],
        "Content-Type": "application/json",
    }
    payload = {"messages": messages, "max_tokens": 256}

    for _ in range(5):
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 429:
            retry_after = (
                response.headers.get("Retry-After")
                or response.headers.get("Retry-After-Ms")
            )
            delay = (
                float(retry_after) / 1000.0
                if retry_after and retry_after.isdigit() and int(retry_after) > 1000
                else float(retry_after or 1)
            )
            time.sleep(min(delay, 10))
            continue
        response.raise_for_status()
        return response.json()

    raise RuntimeError("Retries exhausted")
```

#### .NET：Polly を使った 429 リトライ

```csharp
// dotnet add package Polly
// dotnet add package Azure.Identity
using Polly;
using System.Text;
using System.Text.Json;

double GetDelay(HttpResponseMessage response)
{
    if (response.Headers.TryGetValues("Retry-After", out var seconds) &&
        double.TryParse(seconds.FirstOrDefault(), out var sec))
    {
        return sec;
    }

    if (response.Headers.TryGetValues("Retry-After-Ms", out var milliseconds) &&
        double.TryParse(milliseconds.FirstOrDefault(), out var ms))
    {
        return ms / 1000.0;
    }

    return 1.0;
}

var policy = Policy
    .HandleResult<HttpResponseMessage>(resp => (int)resp.StatusCode == 429)
    .WaitAndRetryAsync(5, (retry, context) =>
    {
        var lastResponse = (HttpResponseMessage)context["lastResponse"];
        return TimeSpan.FromSeconds(Math.Min(GetDelay(lastResponse), 10));
    }, (outcome, delay, retry, context) => Task.CompletedTask);

var httpClient = new HttpClient();
httpClient.DefaultRequestHeaders.Add(
    "Ocp-Apim-Subscription-Key",
    Environment.GetEnvironmentVariable("APIM_SUBSCRIPTION_KEY")
);

var requestUri = (
    $"{Environment.GetEnvironmentVariable("APIM_OPENAI_BASE")}/openai/deployments/"
    + $"{Environment.GetEnvironmentVariable("OPENAI_DEPLOYMENT")}/chat/completions"
    + $"?api-version={Environment.GetEnvironmentVariable("OPENAI_API_VERSION")}" 
);

var payload = JsonSerializer.Serialize(new
{
    messages = new[] { new { role = "user", content = "hello" } },
    max_tokens = 256,
});

var response = await policy.ExecuteAsync(async context =>
{
    var httpResponse = await httpClient.PostAsync(
        requestUri,
        new StringContent(payload, Encoding.UTF8, "application/json")
    );
    context["lastResponse"] = httpResponse;
    return httpResponse;
}, new Context());

response.EnsureSuccessStatusCode();
```

> レート配分やクォータ設計は最新の Quotas/Limits を参照。([Microsoft Learn][28])

### 6) 【K/L】ID・ネットワーク設計の要点

* 認証は `DefaultAzureCredential` を基準に Managed Identity / Entra ID を活用。
* Observability を有効化すると Foundry ダッシュボードと App Insights を接続できる。([Microsoft Learn][12])
* Hub/Project の Managed Network・Private Link、Agent Service の VNet 対応を要件に合わせて選択し、OpenAI やデータソースへは Private Endpoint を推奨。([Microsoft Learn][23])

### 付録：Day2 サンプル向けパッケージ導入メモ

```bash
pip install azure-ai-projects azure-ai-agents azure-identity \
            azure-ai-evaluation azure-monitor-query \
            azure-ai-contentsafety azure-monitor-opentelemetry opentelemetry-sdk requests
```

```bash
dotnet add package Azure.AI.Projects --prerelease
dotnet add package Azure.AI.Agents.Persistent --prerelease
dotnet add package Azure.Monitor.Query
dotnet add package Azure.AI.ContentSafety
dotnet add package Azure.Identity
dotnet add package Polly
```

---

## 進行と持ち物（講師ノート）

* **事前準備**：Azureサブスクリプション（Agent Service/AI Search/App Insights）、モデルデプロイ、RAG用の小規模インデックス、APIM（任意）。
* **ライブデモ**：

  * *Day1*：最小Agent→RAG→Logic Appsツール呼び出し。
  * *Day2*：Connected Agents→Prompt flow評価→Observability→APIMトークンレート制限。
* **トラブル時の代替**：Portal中心の手順で実演→後でコード提示に切替。
* **留意**：レートや機能は随時更新されるため、**最新のQuotas/Limits**と**公式のHow-to/FAQ**を常に参照（スライド末尾に短縮URLを付与）。([Microsoft Learn][28])

---

### 参考リンク（セクションで使用）

* Agent Service 概要/FAQ/クイックスタート：([Microsoft Learn][1])
* ツール（Azure AI Search/全体）：([Microsoft Learn][7])
* Connected Agents：([Microsoft Learn][10])
* Agentic Retrieval（AI Search）：([Microsoft Learn][8])
* Prompt flow（評価/バッチ）：([Microsoft Learn][13])
* Observability（App Insights統合）：([Microsoft Learn][12])
* Content Safety（製品/ポータル）：([Microsoft Azure][20], [Microsoft Learn][19])
* RBAC/ID：([Microsoft Learn][6])
* ネットワーク（Managed Network/Private Link/Agent VNet/On Your Data）：([Microsoft Learn][23])
* Quotas/Limits・割当：([Microsoft Learn][28])
* APIM Token Limit & レート制御：([Microsoft Learn][30])

---

### 次のアクション（ご希望があれば）

* この設計に沿って**PPTテンプレ（章立て・占い枠・図版プレースホルダ・脚注）**を即時生成できます。
* 参加者の技術スタックに合わせて**Python/.NET**どちらでもコード断片を差し込み可能（同じ構成で提示）。

このまま資料化に進めますか？配布形式（日本語／英語併記、PPT/Google Slides）や、社内データでのRAGデモ素材の有無を教えて頂ければ、スライドに具体的な名称・スクショ差し込み位置まで落とし込みます。

[1]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview "What is Azure AI Foundry Agent Service?"
[2]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/assistants "Azure OpenAI Assistants API (Preview)"
[3]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/faq "Azure AI Foundry Agent Service frequently asked questions"
[4]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/overview "What are tools in Azure AI Foundry Agent Service"
[5]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/quickstart "Quickstart - Create a new Azure AI Foundry Agent Service ..."
[6]: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry "Role-based access control for Azure AI Foundry"
[7]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/azure-ai-search "How to use an existing AI Search index with the Azure AI ..."
[8]: https://learn.microsoft.com/en-us/azure/search/search-agentic-retrieval-how-to-pipeline "Build an agentic retrieval solution - Azure AI Search"
[9]: https://azure.microsoft.com/en-us/products/ai-foundry/agent-service/ "Azure AI Foundry Agent Service"
[10]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/connected-agents "How to use connected agents - Azure AI Foundry"
[11]: https://learn.microsoft.com/en-us/semantic-kernel/concepts/planning "What are Planners in Semantic Kernel"
[12]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/monitor-applications "Monitor your Generative AI Applications - Azure AI Foundry"
[13]: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/prompt-flow "Prompt flow in Azure AI Foundry portal"
[14]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/flow-bulk-test-evaluation "Submit batch run and evaluate a flow - Azure AI Foundry"
[15]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/flow-develop-evaluation "Develop an evaluation flow in Azure AI Foundry portal"
[16]: https://azure.github.io/slm-innovator-lab/3_3_1_evaluation/ "Lab 3.3.1 Evaluate your models using Prompt Flow (UI)"
[17]: https://techcommunity.microsoft.com/blog/aiplatformblog/continuously-monitor-your-genai-application-with-azure-ai-foundry-and-azure-moni/4303450 "Continuously monitor your GenAI application with Azure AI ..."
[18]: https://www.dynatrace.com/hub/detail/azure-ai-foundry/ "Azure AI Foundry monitoring & observability | Dynatrace Hub"
[19]: https://learn.microsoft.com/en-us/azure/ai-foundry/ai-services/content-safety-overview "Content Safety in Azure AI Foundry portal overview"
[20]: https://azure.microsoft.com/en-us/products/ai-services/ai-content-safety "Azure AI Content Safety"
[21]: https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/securely-build-and-manage-agents-in-azure-ai-foundry/4415186 "Securely Build and Manage Agents in Azure AI Foundry"
[22]: https://learn.microsoft.com/en-us/azure/ai-services/authentication "Authenticate requests to Azure AI services"
[23]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/configure-managed-network "How to set up a managed network for Azure AI Foundry hubs"
[24]: https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/built-in-enterprise-readiness-with-azure-ai-agent-service/4386541 "Built-in Enterprise Readiness with Azure AI Agent Service"
[25]: https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/virtual-networks "How to use a virtual network with the Azure AI Foundry ..."
[26]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/network "Securing Azure OpenAI inside a virtual network with private ..."
[27]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/on-your-data-configuration "Network and access configuration for Azure OpenAI On ..."
[28]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/quotas-limits "Azure OpenAI in Azure AI Foundry Models Quotas and Limits"
[29]: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/quota "Manage Azure OpenAI in Azure AI Foundry Models quota"
[30]: https://learn.microsoft.com/en-us/azure/api-management/azure-openai-token-limit-policy "Limit Azure OpenAI API token usage"
[31]: https://learn.microsoft.com/en-us/azure/api-management/api-management-sample-flexible-throttling "Advanced Request Throttling with Azure API Management"
[32]: https://learn.microsoft.com/en-us/azure/ai-foundry/ "Azure AI Foundry documentation"
[34]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents "Continuously Evaluate your AI agents"
[36]: https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/evaluate-sdk "Local evaluation with the Azure AI Evaluation SDK"
[37]: https://learn.microsoft.com/en-us/dotnet/api/azure.ai.projects.evaluations.createagentevaluation "Evaluations.CreateAgentEvaluation Method"
[38]: https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-configuration "Configure Azure Monitor OpenTelemetry"
[39]: https://learn.microsoft.com/en-us/samples/azure/azure-sdk-for-python/query-azuremonitor-samples/ "Azure Monitor Query client library Python samples"
[40]: https://learn.microsoft.com/en-us/python/api/overview/azure/ai-contentsafety-readme "Azure AI Content Safety client library for Python"
[41]: https://learn.microsoft.com/en-us/dotnet/api/overview/azure/ai.contentsafety-readme "Azure AI Content Safety client library for .NET"
