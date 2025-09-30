# Azure AI Agent Build and Manage Workshop

[![English](https://img.shields.io/badge/🌐-English-blue.svg)](./README.md)
[![日本語](https://img.shields.io/badge/🌐-日本語-red.svg)](./README.ja.md)

Azure AI Foundry Agent Service を使用してプロダクション対応の AI エージェントを構築、評価、管理するための包括的な2日間のワークショップです。

## 🎯 ワークショップの目標

このワークショップでは、参加者に以下の実践的な経験を提供します：

1. **Agentic AI の基礎理解** - 核となる概念、ツール、Azure AI Agent Service のアーキテクチャ
2. **最小エージェントの構築** - 基本的な会話から RAG 対応、ツール呼び出しエージェントまで
3. **プロダクション対応** - 評価、観測性、セキュリティ、運用のベストプラクティス

## 📚 ワークショップ構成

### Day 1: "エージェントの構築と実行" (4時間)
- **モジュール A-C**: Agentic AI の概念、Azure AI Agent Service の基礎、ハンズオン "Hello Agent"
- **モジュール D-F**: Azure AI Search を使った RAG、Logic Apps ツール統合、Connected Agents（マルチエージェントパターン）

### Day 2: "評価、セキュリティ、運用" (4時間)
- **モジュール G-I**: 高度なマルチエージェントパターン、Prompt flow 評価、Application Insights による観測性
- **モジュール J-M**: Content Safety、RBAC とアイデンティティ、ネットワーク分離、クォータとレート制限、コスト最適化

> 📖 **詳細なカリキュラム**:
> - English: [docs/en/workshop-structure.md](./docs/en/workshop-structure.md)
> - Japanese: [docs/ja/workshop-structure.md](./docs/ja/workshop-structure.md)

## 🚀 クイックスタート

### オプション 1: GitHub Codespaces (推奨)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ChibaYuki347/azure-ai-agent-workshop)

🧪 **テスト済み・検証済み**: すべてのPythonサンプルがテストされ、正常に動作することを確認済みです。

1. 上記の **"Open in GitHub Codespaces"** ボタンをクリック
2. 環境のセットアップを待機（2-3分）
3. すべての依存関係が自動的にインストールされます
4. [手動設定](#2-手動設定) セクションにジャンプ

### オプション 2: ローカル開発

#### 前提条件

- 以下に十分なクォータを持つ Azure サブスクリプション：
  - Azure OpenAI (GPT-4o, GPT-4o-mini)
  - Azure AI Search (Standard ティア)
  - Azure AI Agent Service
- Bicep サポート付き Azure CLI 2.72.0+
- Visual Studio Code または任意のエディタ
- Python 3.8+ または .NET 6+（選択したサンプルに応じて）

### 1. インフラセットアップ

Bicep を使用してワークショップのインフラをデプロイ：

```bash
# リポジトリをクローン
git clone https://github.com/ChibaYuki347/azure-ai-agent-workshop.git
cd azure-ai-agent-workshop

# ログインとサブスクリプション設定
az login
az account set --subscription <your-subscription-id>

# リソースグループ作成
az group create --name rg-aiagent-workshop-dev --location japaneast

# インフラデプロイ
az deployment group create \
  --resource-group rg-aiagent-workshop-dev \
  --template-file infra/main.bicep \
  --parameters @infra/main.parameters.json \
  --parameters adminObjectId=<your-azure-ad-object-id>
```

> 📋 **インフラの詳細**: 完全なデプロイガイドとデプロイ後の手順については [infra/README.md](./infra/README.md) を参照

### 2. 手動設定

Bicep デプロイ後、以下の手動手順を完了：

1. **Azure AI Foundry Hub & Project**（ARM サポートが利用可能になるまで）:
   ```bash
   az ai hub create --name aifoundry-hub-dev --resource-group rg-aiagent-workshop-dev
   az ai project create --name aifoundry-project-dev --hub-name aifoundry-hub-dev --resource-group rg-aiagent-workshop-dev
   ```

2. **AI Agent Service 接続**: Azure ポータルで AI Agent Service アカウントを開き、Entra ID 認証を使用して Azure OpenAI 接続を手動で作成

3. **AI Search インデックス**: サンプルドキュメントをアップロードし、RAG シナリオ用の検索インデックスを作成

### 3. ワークショップサンプルの実行

お好みの言語を選択してサンプルに従ってください：

#### Python サンプル

```bash
cd samples/python
pip install -r requirements.txt

# 基本エージェント会話
python 01_basic_agent/main.py

# RAG 対応エージェント（AI Search 連携）
python 02_ai_search_rag/main.py

# Connected Agents ワークフロー（リサーチ → 分析 → レポート作成）
python 04_connected_agents/main.py
```

#### C# サンプル
```bash
cd samples/csharp
dotnet restore

# 基本エージェント会話
dotnet run --project BasicAgent

# RAG 対応エージェント
dotnet run --project RagAgent

# ツール呼び出しエージェント
dotnet run --project ToolAgent
```

## 📁 リポジトリ構造

```
├── README.md                          # このファイル
├── README.ja.md                       # 日本語版
├── docs/                              # ワークショップドキュメント
│   ├── en/                           # 英語ドキュメント
│   │   └── workshop-structure.md     # 詳細カリキュラム
│   └── ja/                           # 日本語ドキュメント
│       └── workshop-structure.md     # 詳細カリキュラム
├── infra/                            # Infrastructure as Code
│   ├── main.bicep                    # メイン Bicep テンプレート
│   ├── main.parameters.json          # デプロイパラメータ
│   ├── logic-app-definition.json     # Logic App ワークフロー
│   └── README.md                     # インフラガイド
└── samples/                          # ワークショップコードサンプル
    ├── python/                       # Python サンプル
    │   ├── basic_agent.py           # 基本エージェント例
    │   ├── rag_agent.py             # RAG 対応エージェント
    │   ├── tool_agent.py            # ツール呼び出しエージェント
    │   └── requirements.txt         # Python 依存関係
    └── csharp/                       # C# サンプル
        ├── BasicAgent/              # 基本エージェントプロジェクト
        ├── RagAgent/                # RAG エージェントプロジェクト
        └── ToolAgent/               # ツールエージェントプロジェクト
```

## 🔧 デプロイされるコンポーネント

Bicep テンプレートでプロビジョニングされるもの：

| コンポーネント | 目的 | 備考 |
|-----------|---------|-------|
| **Azure AI Agent Service** | GPT-4o/4o-mini デプロイメント付きの管理されたエージェントランタイム | カスタム RAI ポリシー、プロジェクト管理 |
| **Azure OpenAI** | エージェント用のモデルサービング | コンテンツセーフティ付き GPT-4 デプロイメント |
| **Azure AI Search** | RAG ナレッジ検索 | セマンティック検索付き Standard ティア |
| **Logic App Standard** | 外部ツール統合 | エージェントツール呼び出し用 HTTP トリガー |
| **Key Vault** | シークレットと接続文字列 | RBAC セキュアアクセス |
| **Application Insights** | 観測性と監視 | エージェント会話追跡 |
| **API Management** | レート制限とアクセス制御 | オプションのトークンベース スロットリング |

## 🎓 学習パス

### 開発者向け
- `samples/python/basic_agent.py` または `samples/csharp/BasicAgent` から開始
- RAG とツール統合サンプルを進行
- Day 2 モジュールの評価フローを探索

### アーキテクト向け
- `infra/main.bicep` のインフラ設計を確認
- ネットワーク分離とセキュリティモジュール（Day 2）に焦点
- マルチエージェントパターンと Connected Agents を学習

### 運用者向け
- 観測性セットアップとダッシュボードを調査
- クォータ管理とコスト最適化を学習
- Content Safety と RBAC 設定で練習

## 🛟 トラブルシューティング

### よくある問題
- **デプロイ中の RequestConflict**: Azure AI Agent Service 操作が競合。5-10分待ってから再試行。
- **モデルデプロイクォータ**: リージョンで GPT-4o モデルに十分な TPM クォータがあることを確認。
- **Logic App ツールエラー**: `triggerBody()` 式が JSON スキーマと一致することを確認。

### ヘルプの取得
- デプロイトラブルシューティングは [infra/README.md](./infra/README.md) を確認
- Azure AI Agent Service [公式ドキュメント](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/) を確認
- ワークショップ固有の問題についてはこのリポジトリで Issue を開いてください

## 🌐 言語

- **English**: プライマリドキュメント言語
- **日本語**: [README.ja.md](./README.ja.md) と `docs/ja/` で完全な日本語翻訳が利用可能

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🤝 貢献

貢献を歓迎します！ワークショップコンテンツ、インフラテンプレート、またはサンプルコードの改善について、プルリクエストの送信や Issue の開示をお気軽にどうぞ。

---

**インテリジェントエージェントを構築する準備はできましたか？** 上記のインフラセットアップから始めて、サンプルに飛び込みましょう！ 🚀