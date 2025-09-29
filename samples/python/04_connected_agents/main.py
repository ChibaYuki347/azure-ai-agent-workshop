"""
Connected Agents Orchestration Example
Research → Analysis → Writing Agent Workflow

This example demonstrates how to use Azure AI Agent Service with Connected Agents
to implement a multi-agent workflow for research, analysis, and report writing.
"""

import os
import asyncio
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from azure.ai.foundry.agents import AgentClient
from azure.identity import DefaultAzureCredential

@dataclass
class ResearchRequest:
    """Structure for research requests"""
    topic: str
    scope: str = "comprehensive"
    time_period: Optional[str] = None
    language: str = "English"
    depth: str = "moderate"
    sources_required: int = 5

@dataclass 
class WorkflowResult:
    """Structure for workflow results"""
    success: bool
    research_data: Optional[Dict[str, Any]] = None
    analysis_results: Optional[Dict[str, Any]] = None
    final_report: Optional[str] = None
    error_message: Optional[str] = None

class ConnectedAgentsOrchestrator:
    """
    Orchestrates a multi-agent workflow for research, analysis, and writing.
    
    This class coordinates three specialized agents:
    - Research Agent: Gathers information from web sources
    - Analysis Agent: Analyzes and synthesizes research data  
    - Writing Agent: Creates formatted reports
    """
    
    def __init__(self, project_connection_string: str):
        """
        Initialize the orchestrator with Azure AI connection.
        
        Args:
            project_connection_string: Azure AI Foundry project connection string
        """
        self.credential = DefaultAzureCredential()
        self.client = AgentClient.from_connection_string(
            project_connection_string,
            credential=self.credential
        )
        
        # Agent IDs - these should be created in Azure AI Foundry first
        self.research_agent_id = "research-agent"
        self.analysis_agent_id = "analysis-agent" 
        self.writing_agent_id = "writing-agent"
        
    async def execute_research_workflow(
        self, 
        request: ResearchRequest,
        report_format: str = "business_report"
    ) -> WorkflowResult:
        """
        Execute the complete research workflow.
        
        Args:
            request: Research request parameters
            report_format: Desired output format (business_report, academic_paper, blog_post)
            
        Returns:
            WorkflowResult containing all outputs or error information
        """
        try:
            # Step 1: Research Phase
            print(f"🔍 Starting research on: {request.topic}")
            research_data = await self._execute_research_phase(request)
            
            if not research_data:
                return WorkflowResult(
                    success=False,
                    error_message="Research phase failed to gather sufficient data"
                )
            
            # Step 2: Analysis Phase  
            print("📊 Analyzing research data...")
            analysis_results = await self._execute_analysis_phase(research_data)
            
            if not analysis_results:
                return WorkflowResult(
                    success=False,
                    research_data=research_data,
                    error_message="Analysis phase failed to process research data"
                )
            
            # Step 3: Writing Phase
            print("📝 Generating final report...")
            final_report = await self._execute_writing_phase(
                analysis_results, 
                report_format
            )
            
            if not final_report:
                return WorkflowResult(
                    success=False,
                    research_data=research_data,
                    analysis_results=analysis_results,
                    error_message="Writing phase failed to generate report"
                )
            
            print("✅ Workflow completed successfully!")
            return WorkflowResult(
                success=True,
                research_data=research_data,
                analysis_results=analysis_results,
                final_report=final_report
            )
            
        except Exception as e:
            return WorkflowResult(
                success=False,
                error_message=f"Workflow error: {str(e)}"
            )
    
    async def _execute_research_phase(self, request: ResearchRequest) -> Optional[Dict[str, Any]]:
        """Execute research phase using Research Agent."""
        
        research_prompt = f"""
        Please conduct comprehensive research on the following topic:
        
        Topic: {request.topic}
        Scope: {request.scope}
        Time Period: {request.time_period or "Recent developments"}
        Language: {request.language}
        Depth: {request.depth}
        Minimum Sources: {request.sources_required}
        
        Please provide:
        1. A summary of key findings
        2. List of credible sources with URLs
        3. Important data points and statistics
        4. Different perspectives or viewpoints
        5. Any limitations or gaps in available information
        
        Format your response as structured data that can be easily processed
        by the analysis agent.
        """
        
        try:
            # Create thread for research agent
            research_thread = self.client.create_thread()
            
            # Send research request
            message = self.client.create_message(
                thread_id=research_thread.id,
                role="user",
                content=research_prompt
            )
            
            # Run the research agent
            run = self.client.create_run(
                thread_id=research_thread.id,
                agent_id=self.research_agent_id
            )
            
            # Wait for completion
            completed_run = self.client.wait_for_run(
                thread_id=research_thread.id,
                run_id=run.id
            )
            
            if completed_run.status == "completed":
                # Get the research results
                messages = self.client.list_messages(
                    thread_id=research_thread.id,
                    order="desc",
                    limit=1
                )
                
                if messages and messages[0].role == "assistant":
                    research_content = messages[0].content[0].text.value
                    return {
                        "raw_content": research_content,
                        "thread_id": research_thread.id,
                        "request_params": request.__dict__
                    }
            
            return None
            
        except Exception as e:
            print(f"Research phase error: {e}")
            return None
    
    async def _execute_analysis_phase(self, research_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute analysis phase using Analysis Agent."""
        
        analysis_prompt = f"""
        Please analyze the following research data and provide structured insights:
        
        Research Content:
        {research_data['raw_content']}
        
        Please provide:
        1. Key themes and patterns identified
        2. Comparative analysis of different sources/viewpoints
        3. Strengths and weaknesses of the findings
        4. Causal relationships or correlations discovered
        5. Gaps in knowledge or contradictory information
        6. Strategic insights and implications
        7. Recommendations for further investigation
        
        Structure your analysis so it can be easily used by a writing agent
        to create a comprehensive report.
        """
        
        try:
            # Create thread for analysis agent
            analysis_thread = self.client.create_thread()
            
            # Send analysis request
            message = self.client.create_message(
                thread_id=analysis_thread.id,
                role="user", 
                content=analysis_prompt
            )
            
            # Run the analysis agent
            run = self.client.create_run(
                thread_id=analysis_thread.id,
                agent_id=self.analysis_agent_id
            )
            
            # Wait for completion
            completed_run = self.client.wait_for_run(
                thread_id=analysis_thread.id,
                run_id=run.id
            )
            
            if completed_run.status == "completed":
                # Get the analysis results
                messages = self.client.list_messages(
                    thread_id=analysis_thread.id,
                    order="desc",
                    limit=1
                )
                
                if messages and messages[0].role == "assistant":
                    analysis_content = messages[0].content[0].text.value
                    return {
                        "analysis_content": analysis_content,
                        "thread_id": analysis_thread.id,
                        "source_research": research_data
                    }
            
            return None
            
        except Exception as e:
            print(f"Analysis phase error: {e}")
            return None
    
    async def _execute_writing_phase(
        self, 
        analysis_results: Dict[str, Any], 
        report_format: str
    ) -> Optional[str]:
        """Execute writing phase using Writing Agent."""
        
        format_instructions = {
            "business_report": """
            Create a professional business report with:
            - Executive Summary
            - Background/Context
            - Key Findings
            - Analysis & Insights
            - Recommendations
            - Conclusion
            Use clear headings, bullet points, and professional tone.
            """,
            "academic_paper": """
            Create an academic-style paper with:
            - Abstract
            - Introduction
            - Literature Review/Background
            - Methodology (research approach)
            - Results/Findings
            - Discussion
            - Conclusion
            - References
            Use formal academic tone with proper citations.
            """,
            "blog_post": """
            Create an engaging blog post with:
            - Compelling headline
            - Introduction hook
            - Main content with subheadings
            - Key takeaways
            - Call to action
            Use conversational tone and engaging style.
            """
        }
        
        writing_prompt = f"""
        Please create a comprehensive report based on the following analysis:
        
        Analysis Results:
        {analysis_results['analysis_content']}
        
        Report Format: {report_format}
        
        Format Instructions:
        {format_instructions.get(report_format, format_instructions['business_report'])}
        
        Please ensure:
        - All key points from the analysis are covered
        - The report flows logically
        - Sources are referenced where appropriate
        - The tone matches the requested format
        - The content is well-structured and professional
        """
        
        try:
            # Create thread for writing agent
            writing_thread = self.client.create_thread()
            
            # Send writing request
            message = self.client.create_message(
                thread_id=writing_thread.id,
                role="user",
                content=writing_prompt
            )
            
            # Run the writing agent
            run = self.client.create_run(
                thread_id=writing_thread.id,
                agent_id=self.writing_agent_id
            )
            
            # Wait for completion
            completed_run = self.client.wait_for_run(
                thread_id=writing_thread.id,
                run_id=run.id
            )
            
            if completed_run.status == "completed":
                # Get the final report
                messages = self.client.list_messages(
                    thread_id=writing_thread.id,
                    order="desc",
                    limit=1
                )
                
                if messages and messages[0].role == "assistant":
                    return messages[0].content[0].text.value
            
            return None
            
        except Exception as e:
            print(f"Writing phase error: {e}")
            return None

async def main():
    """
    Example usage of the Connected Agents orchestrator.
    """
    # Configuration
    project_connection_string = os.getenv("AZURE_AI_PROJECT_CONNECTION_STRING")
    if not project_connection_string:
        print("❌ Please set AZURE_AI_PROJECT_CONNECTION_STRING environment variable")
        return
    
    # Initialize orchestrator
    orchestrator = ConnectedAgentsOrchestrator(project_connection_string)
    
    # Define research request
    research_request = ResearchRequest(
        topic="Impact of Artificial Intelligence on Supply Chain Management",
        scope="comprehensive",
        time_period="2022-2024",
        language="English",
        depth="detailed",
        sources_required=8
    )
    
    # Execute workflow
    print("🚀 Starting Connected Agents workflow...")
    result = await orchestrator.execute_research_workflow(
        request=research_request,
        report_format="business_report"
    )
    
    # Handle results
    if result.success:
        print("✅ Workflow completed successfully!")
        print("\n" + "="*50)
        print("FINAL REPORT")
        print("="*50)
        print(result.final_report)
        
        # Optionally save to file
        with open("connected_agents_report.md", "w", encoding="utf-8") as f:
            f.write(result.final_report)
        print(f"\n📄 Report saved to: connected_agents_report.md")
        
    else:
        print(f"❌ Workflow failed: {result.error_message}")
        
        # Show partial results if available
        if result.research_data:
            print("\n📊 Research data was collected successfully")
        if result.analysis_results:
            print("📈 Analysis was completed successfully")

if __name__ == "__main__":
    asyncio.run(main())