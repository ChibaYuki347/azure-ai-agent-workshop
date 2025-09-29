# Connected Agents: Research → Analysis → Writing Pattern

This example demonstrates how to use **Azure AI Agent Service Connected Agents** to implement a multi-agent workflow for research, analysis, and report writing.

## Architecture Overview

```
User Request
     ↓
Main Agent (Orchestrator)
     ↓
Research Agent → Analysis Agent → Writing Agent
     ↓                ↓              ↓
  Web Search    Data Analysis   Report Generation
     ↓                ↓              ↓
     └────────────────┴──────────────┘
                     ↓
               Final Report
```

## Agent Roles

| Agent | Responsibility | Input | Output | Tools |
|-------|---------------|-------|--------|-------|
| **Main Agent** | Orchestrates workflow, manages user interaction | User requirements | Final report | Connected Agents |
| **Research Agent** | Information gathering from web sources | Research topic, keywords | Structured research data | Bing Search, Deep Research |
| **Analysis Agent** | Data analysis, comparison, insights | Research results | Analysis insights | Python execution, calculations |
| **Writing Agent** | Report composition and formatting | Analysis results | Formatted report | Text generation, citations |

## Implementation Steps

### 1. Create Individual Agents

First, create each specialized agent in Azure AI Foundry:

#### Research Agent Configuration
```json
{
  "name": "research-agent",
  "description": "Information gathering specialist using web search and research tools",
  "instructions": "You are a Research Agent specialized in gathering information from credible sources...",
  "tools": ["bing_search", "deep_research"],
  "model": "gpt-4o"
}
```

#### Analysis Agent Configuration
```json
{
  "name": "analysis-agent", 
  "description": "Data analysis and insight generation specialist",
  "instructions": "You are an Analysis Agent that processes research data to extract insights...",
  "tools": ["python_code_interpreter"],
  "model": "gpt-4o"
}
```

#### Writing Agent Configuration
```json
{
  "name": "writing-agent",
  "description": "Report writing and document formatting specialist", 
  "instructions": "You are a Writing Agent that creates well-structured reports...",
  "tools": [],
  "model": "gpt-4o"
}
```

### 2. Configure Connected Agents

In the Main Agent, add the three agents as Connected Agents:

1. Go to Azure AI Foundry portal
2. Open your Main Agent
3. Navigate to "Connected Agents" tab
4. Add each agent with delegation instructions:

**Research Agent Connection:**
- **When to use**: "When the user asks for research, information gathering, or fact-finding about any topic"
- **Instructions**: "Delegate research tasks to gather comprehensive information with proper citations"

**Analysis Agent Connection:**
- **When to use**: "When research data needs analysis, comparison, or insight extraction"
- **Instructions**: "Analyze research findings to identify patterns, relationships, and key insights"

**Writing Agent Connection:**
- **When to use**: "When analysis results need to be formatted into a coherent report"
- **Instructions**: "Create well-structured reports with proper formatting and citations"

### 3. Main Agent Orchestration

The Main Agent follows this workflow:

```python
# Pseudo-code for Main Agent logic
def handle_user_request(user_input):
    # 1. Parse user requirements
    requirements = parse_requirements(user_input)
    
    # 2. Delegate to Research Agent
    research_results = call_connected_agent(
        "research-agent", 
        f"Research topic: {requirements.topic}"
    )
    
    # 3. Delegate to Analysis Agent  
    analysis_results = call_connected_agent(
        "analysis-agent",
        f"Analyze this research data: {research_results}"
    )
    
    # 4. Delegate to Writing Agent
    final_report = call_connected_agent(
        "writing-agent", 
        f"Create report from analysis: {analysis_results}"
    )
    
    return final_report
```

## Agent Instructions

### Research Agent Instructions

**English:**
```
You are the "Research Agent."
Your role is to perform comprehensive information gathering using tools such as Bing Search or Azure's Deep Research. Given a user's theme or keywords, you should collect relevant, credible sources and return structured research output.

**Output format:**
- Theme / subthemes
- Bibliography (title, author, year, URL or DOI) 
- Key points or summary (3–5 sentences) per source
- Discovered claims, numerical data, trends
- Caveats & limitations (reliability concerns, conflicting info)

Always include proper source attribution (URLs, DOIs) whenever possible.
If the user specifies period, language, or depth requirements, follow those constraints.
```

**Japanese:**
```
あなたは "Research Agent" です。
あなたの役割は、与えられたテーマ・キーワードをもとに、信頼できる情報源を Bing 検索や Deep Research ツールを使って調べ、構造化された調査結果を返すことです。

【出力形式】
- テーマ／サブテーマ
- 出典一覧（タイトル、著者、発行年、URL／DOI）
- 各出典の要点・要約（3〜5行程度）
- 見つかった主張・数値データ・傾向
- 注意点・限界（情報の信頼性、矛盾点など）

出典を必ず明示し、URL や DOI を可能な限り付与してください。
調査対象の期間、言語、深掘りレベルについて指示があれば従ってください。
```

### Analysis Agent Instructions

**English:**
```
You are the "Analysis Agent."
Your role is to take research output and perform deeper analytical work, such as:

- Organizing key points and themes
- Conducting comparative analysis: highlighting consistencies, discrepancies, and relationships among sources
- Identifying causal relationships or contributing factors  
- Generating hypotheses, insights, and implications
- Performing basic statistical summaries or suggesting charts/tables when appropriate

Present your output in a structured format with sections such as "Analysis Results," "Insights / Implications," "Open Questions / Limitations," so that the Writing Agent can easily consume it.
```

**Japanese:**
```
あなたは "Analysis Agent" です。
あなたの役割は、Research Agent から提供された調査結果をもとに、以下のような分析を行うことです：

- 論点整理：主要なテーマや争点を抽出
- 比較分析：異なる出典間の関係性や矛盾点を対比
- 因果関係・要因分析
- 仮説や示唆の提示
- 必要であれば簡単な統計処理、グラフ案提示も可

出力は構造化された形式で、後続の Writing Agent が取り込みやすいように、「分析結果」「示唆」「未解明点」などのセクションに分けてください。
```

### Writing Agent Instructions

**English:**
```
You are the "Writing Agent."
Your role is to take analysis output and produce a polished report or document in the user's desired style/format.

**Input provided:**
- Analytical results, insights, open questions, structural outline

**Output requirements:**
- Structure: Introduction / Background / Method / Findings / Interpretation / Conclusion & Recommendations
- Logical flow and section headings
- Proper citation / footnotes for sources
- Table/figure suggestions if applicable
- Tone/style specification (academic, business, accessible prose)

If the user specifies a format (academic paper, business report, blog post), adhere to that format.
```

**Japanese:**
```
あなたは "Writing Agent" です。
あなたの役割は、Analysis Agent が構成した分析アウトプットを元に、指定スタイル・形式でレポートや文章を作成することです。

【入力情報】
- 分析結果、示唆、未解明点、構成案など

【出力要件例】
- 目的（イントロ）、背景、方法、見解、結論・提言
- 適切な見出し構成と流れ
- 引用・脚注（出典の明示）
- 図表・グラフ案（あれば）
- 語調指定（学術調、ビジネス調、平易な文章など）

ユーザーからフォーマット（例：ビジネスレポート、論文形式、ブログ記事形式など）の指定があれば、それに従ってください。
```

### Main Agent Instructions

**English:**
```
You are the "Main Agent" (orchestrator).
You coordinate sub-agents to complete research and reporting tasks as follows:

1. Parse user instructions: theme, objective, format, constraints (time period, language, depth)
2. Delegate to Research Agent: send a research task, get back structured research output
3. Delegate to Analysis Agent: send the research output, get back analytical insights
4. Delegate to Writing Agent: send the analysis output, get back the final written report
5. Optionally, ask the user for intermediate confirmation (e.g. outline approval)
6. Return the final report to the user

Ensure that the sub-task instructions you send to each agent match the expected input format of that agent.
```

**Japanese:**
```
あなたは "Main Agent"（統括エージェント）です。
ユーザーから来る指示を理解し、以下の流れでサブエージェントにタスクを割り振って統合出力を返してください。

1. ユーザーからテーマ、目的、形式、制約（期間、言語、深さなど）を取得
2. Research Agent にリサーチタスクを割り振り、調査結果を受け取る
3. Analysis Agent に分析タスクを割り振り、分析アウトプットを受け取る
4. Writing Agent に文章生成タスクを割り振り、最終レポートを得る
5. 必要なら中間ステップでユーザーに確認（例：構成案確認など）
6. 最終レポートをユーザーに返却

各サブエージェントへのタスク指示は、そのエージェントの期待入力形式に従って構成してください。
```

## Implementation Considerations

### Tool Configuration
- **Research Agent**: Attach Bing Search and Deep Research tools for web information gathering
- **Analysis Agent**: Attach Python Code Interpreter for statistical analysis and calculations
- **Writing Agent**: No special tools needed, focuses on text generation and formatting

### Data Flow Format
Consider using structured JSON for inter-agent communication:

```json
{
  "research_output": {
    "theme": "AI in Healthcare",
    "sources": [...],
    "key_findings": [...],
    "limitations": [...]
  },
  "analysis_output": {
    "key_themes": [...],
    "insights": [...],
    "recommendations": [...]
  }
}
```

### Error Handling
- Handle cases where research returns insufficient data
- Manage conflicting information from sources
- Provide fallback strategies for failed tool calls
- Include confidence levels in outputs

### Monitoring & Observability
- Track execution time for each agent
- Monitor tool usage and success rates
- Log intermediate outputs for debugging
- Measure overall workflow success metrics

## Usage Examples

### Business Research Example
```
User: "Research the impact of AI on supply chain management and create a business report"

Main Agent Flow:
1. Research Agent → Gathers sources on AI supply chain applications
2. Analysis Agent → Analyzes trends, benefits, challenges, ROI data  
3. Writing Agent → Creates executive summary with recommendations
```

### Academic Research Example
```
User: "Investigate recent developments in quantum computing algorithms for a literature review"

Main Agent Flow:
1. Research Agent → Searches academic papers, conferences, patents
2. Analysis Agent → Categorizes approaches, compares methodologies
3. Writing Agent → Formats as academic literature review with citations
```

## References

- [Azure AI Foundry Connected Agents Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/connected-agents)
- [Deep Research Tool Guide](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/deep-research-samples)
- [Agent Service Overview](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview)