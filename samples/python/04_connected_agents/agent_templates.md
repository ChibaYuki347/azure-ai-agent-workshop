# Azure AI Agent Configuration Templates

This directory contains configuration templates for setting up Connected Agents in Azure AI Foundry.

## Agent Configuration Files

### Research Agent Configuration

```json
{
  "name": "research-agent",
  "description": "Information gathering specialist using web search and research tools",
  "instructions": "You are the Research Agent. Your role is to perform comprehensive information gathering using tools such as Bing Search or Azure's Deep Research. Given a user's theme or keywords, you should collect relevant, credible sources and return structured research output.\n\nOutput format:\n- Theme / subthemes\n- Bibliography (title, author, year, URL or DOI)\n- Key points or summary (3–5 sentences) per source\n- Discovered claims, numerical data, trends\n- Caveats & limitations (reliability concerns, conflicting info)\n\nAlways include proper source attribution (URLs, DOIs) whenever possible. If the user specifies period, language, or depth requirements, follow those constraints.",
  "model": "gpt-4o",
  "tools": [
    {
      "type": "bing_grounding"
    },
    {
      "type": "deep_research"
    }
  ],
  "temperature": 0.7,
  "top_p": 0.9
}
```

### Analysis Agent Configuration

```json
{
  "name": "analysis-agent",
  "description": "Data analysis and insight generation specialist",
  "instructions": "You are the Analysis Agent. Your role is to take research output and perform deeper analytical work, such as:\n\n- Organizing key points and themes\n- Conducting comparative analysis: highlighting consistencies, discrepancies, and relationships among sources\n- Identifying causal relationships or contributing factors\n- Generating hypotheses, insights, and implications\n- Performing basic statistical summaries or suggesting charts/tables when appropriate\n\nPresent your output in a structured format with sections such as 'Analysis Results,' 'Insights / Implications,' 'Open Questions / Limitations,' so that the Writing Agent can easily consume it.",
  "model": "gpt-4o",
  "tools": [
    {
      "type": "code_interpreter"
    }
  ],
  "temperature": 0.5,
  "top_p": 0.8
}
```

### Writing Agent Configuration

```json
{
  "name": "writing-agent",
  "description": "Report writing and document formatting specialist",
  "instructions": "You are the Writing Agent. Your role is to take analysis output and produce a polished report or document in the user's desired style/format.\n\nInput provided:\n- Analytical results, insights, open questions, structural outline\n\nOutput requirements:\n- Structure: Introduction / Background / Method / Findings / Interpretation / Conclusion & Recommendations\n- Logical flow and section headings\n- Proper citation / footnotes for sources\n- Table/figure suggestions if applicable\n- Tone/style specification (academic, business, accessible prose)\n\nIf the user specifies a format (academic paper, business report, blog post), adhere to that format.",
  "model": "gpt-4o",
  "tools": [],
  "temperature": 0.6,
  "top_p": 0.9
}
```

### Main Orchestrator Agent Configuration

```json
{
  "name": "main-orchestrator",
  "description": "Orchestrates multi-agent workflows for research, analysis, and reporting",
  "instructions": "You are the Main Agent (orchestrator). You coordinate sub-agents to complete research and reporting tasks as follows:\n\n1. Parse user instructions: theme, objective, format, constraints (time period, language, depth)\n2. Delegate to Research Agent: send a research task, get back structured research output\n3. Delegate to Analysis Agent: send the research output, get back analytical insights\n4. Delegate to Writing Agent: send the analysis output, get back the final written report\n5. Optionally, ask the user for intermediate confirmation (e.g. outline approval)\n6. Return the final report to the user\n\nEnsure that the sub-task instructions you send to each agent match the expected input format of that agent.",
  "model": "gpt-4o",
  "tools": [],
  "temperature": 0.3,
  "top_p": 0.8,
  "connected_agents": [
    {
      "agent_id": "research-agent",
      "name": "Research Agent",
      "description": "Gathers information from web sources and research databases",
      "when_to_use": "When the user asks for research, information gathering, or fact-finding about any topic",
      "delegation_instructions": "Delegate research tasks to gather comprehensive information with proper citations. Specify the research topic, scope, time period, and required depth."
    },
    {
      "agent_id": "analysis-agent",
      "name": "Analysis Agent", 
      "description": "Analyzes research data to extract insights and patterns",
      "when_to_use": "When research data needs analysis, comparison, or insight extraction",
      "delegation_instructions": "Analyze research findings to identify patterns, relationships, and key insights. Focus on comparative analysis and hypothesis generation."
    },
    {
      "agent_id": "writing-agent",
      "name": "Writing Agent",
      "description": "Creates well-structured reports and documents",
      "when_to_use": "When analysis results need to be formatted into a coherent report",
      "delegation_instructions": "Create well-structured reports with proper formatting and citations. Specify the desired format (business report, academic paper, blog post) and target audience."
    }
  ]
}
```

## Setup Instructions

### 1. Create Agents in Azure AI Foundry

1. Navigate to Azure AI Foundry portal
2. Go to your project
3. Create each agent using the configurations above:
   - Copy the JSON configuration
   - Create new agent
   - Paste configuration details
   - Assign appropriate tools

### 2. Configure Connected Agents

For the Main Orchestrator agent:

1. Open the Main Orchestrator agent
2. Go to "Connected Agents" tab
3. Add each sub-agent:
   - Research Agent
   - Analysis Agent  
   - Writing Agent
4. Configure delegation rules using the "when_to_use" and "delegation_instructions" from the JSON

### 3. Tool Setup

#### Research Agent Tools
- **Bing Grounding**: Enable web search capabilities
- **Deep Research**: Enable comprehensive research functionality

#### Analysis Agent Tools  
- **Code Interpreter**: Enable Python execution for statistical analysis

#### Writing Agent Tools
- No additional tools required (uses base language model)

### 4. Environment Variables

Set these environment variables for the Python sample:

```bash
export AZURE_AI_PROJECT_CONNECTION_STRING="your_project_connection_string"
```

## Usage Examples

### Business Research Workflow
```python
research_request = ResearchRequest(
    topic="Digital Transformation in Retail Industry",
    scope="comprehensive", 
    time_period="2023-2024",
    language="English",
    depth="detailed",
    sources_required=10
)

result = await orchestrator.execute_research_workflow(
    request=research_request,
    report_format="business_report"
)
```

### Academic Research Workflow
```python
research_request = ResearchRequest(
    topic="Machine Learning Applications in Healthcare Diagnostics",
    scope="academic",
    time_period="2022-2024", 
    language="English",
    depth="detailed",
    sources_required=15
)

result = await orchestrator.execute_research_workflow(
    request=research_request,
    report_format="academic_paper"
)
```

## Best Practices

### Agent Design
- **Single Responsibility**: Each agent has one clear purpose
- **Clear Interfaces**: Well-defined input/output formats
- **Error Handling**: Graceful degradation when tools fail
- **Observability**: Log all agent interactions

### Workflow Design
- **Sequential Processing**: Clear hand-offs between agents
- **Validation Points**: Check outputs before proceeding
- **User Checkpoints**: Allow user confirmation at key stages
- **Rollback Strategy**: Handle partial failures gracefully

### Performance Optimization
- **Parallel Processing**: Run independent operations concurrently
- **Caching**: Store intermediate results for reuse
- **Rate Limiting**: Respect API limits and quotas
- **Monitoring**: Track execution times and success rates

## Troubleshooting

### Common Issues

1. **Agent Not Found**
   - Verify agent IDs match exactly
   - Check agent is deployed and accessible

2. **Tool Execution Failures**
   - Verify tool permissions and quotas
   - Check network connectivity for web search tools

3. **Delegation Errors**
   - Review Connected Agent configuration
   - Verify delegation instructions are clear

4. **Output Format Issues**
   - Check agent instructions for output format
   - Validate intermediate results before passing to next agent

### Debugging Tips

- Enable detailed logging for all agent interactions
- Test each agent individually before connecting them
- Use simple test cases to validate the workflow
- Monitor token usage and execution times