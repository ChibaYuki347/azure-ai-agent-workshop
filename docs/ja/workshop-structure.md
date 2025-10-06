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

## 付録：スライド素材に挿入すべき“図・表・断片コード”テンプレ

* **アーキ図（Day1 S4/S13/S18、Day2 S42–S45）**

  * *図層*：User → Agent Service（Thread/Run/Tools）→（AI Search／Logic Apps／Functions）→ Azure OpenAI → Observability（App Insights） → Entra ID/Network（Private Link/VNet）。
  * 参考：Agent Service概要／ツール概要／Agentic Retrieval／Observability。([Microsoft Learn][1])

* **評価フロー図（Day2 S28–S31）**

  * *要素*：テストセット → Prompt flow（アプリフロー）→ Evaluation flow（メトリクス）→ 比較ダッシュボード。
  * 参考：Prompt flowのEvaluationフロー一式。([Microsoft Learn][13])

* **ネットワーク構成図（Day2 S42–S45）**

  * *要素*：Hub Managed Network／Private Link、Agent VNet（必要に応じてNetwork Injection/BYO VNet）とOpenAI/データソースのPrivate Endpoint。
  * 参考：Managed Network/Private Link/Agent VNet/On Your Dataの各ドキュメント。([Microsoft Learn][23])

* **サンプルコード断片（Day1 S9／Day1 S16）**

  * Agent作成～Runの最小例（Python）と、RAG回答に**引用**を含めるプロンプト指示例。
  * 参考：Agentクイックスタート／AI Search tool how-to。([Microsoft Learn][5])

* **レート制御スニペット（Day2 S48–S49）**

  * APIMの`azure-openai-token-limit-policy`の主要属性（`tokens-per-minute`/`counter-key`/`estimate-prompt-tokens`）の要点だけを抜粋表示。
  * 参考：公式APIMポリシー／GitHubサンプル。([Microsoft Learn][30], [GitHub][33])

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
[33]: https://github.com/microsoft/AzureOpenAI-with-APIM "microsoft/AzureOpenAI-with-APIM"
