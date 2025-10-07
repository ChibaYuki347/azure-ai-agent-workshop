"""Connected Agents demo CLI for the workshop."""

from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from ..common import configure_logging, load_config

app = typer.Typer(help="Connected Agents orchestration demo")
console = Console()


@dataclass(slots=True)
class ResearchRequest:
    topic: str
    scope: str = "comprehensive"
    time_period: Optional[str] = None
    language: str = "English"
    depth: str = "moderate"
    sources_required: int = 5
    output_format: str = "business_report"


@dataclass(slots=True)
class WorkflowArtifacts:
    research_thread: Optional[str] = None
    analysis_thread: Optional[str] = None
    writing_thread: Optional[str] = None
    report_path: Optional[Path] = None


@dataclass(slots=True)
class WorkflowResult:
    success: bool
    message: str
    research_content: Optional[str] = None
    analysis_content: Optional[str] = None
    final_report: Optional[str] = None
    artifacts: WorkflowArtifacts = field(default_factory=WorkflowArtifacts)


class ConnectedAgentsOrchestrator:
    def __init__(self) -> None:
        configure_logging()
        self.config = load_config()
        self.credential = DefaultAzureCredential()
        self.artifacts = WorkflowArtifacts()
        self.client: Optional[AIProjectClient] = None

        self.research_agent_id = self.config.connected_research_agent_id or "research-agent"
        self.analysis_agent_id = self.config.connected_analysis_agent_id or "analysis-agent"
        self.writing_agent_id = self.config.connected_writing_agent_id or "writing-agent"

    def run(self, request: ResearchRequest) -> WorkflowResult:
        try:
            with AIProjectClient(endpoint=self.config.project_endpoint, credential=self.credential) as client:
                self.client = client
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                ) as progress:
                    research_task = progress.add_task("Gathering research", start=False)
                    analysis_task = progress.add_task("Synthesizing insights", start=False)
                    writing_task = progress.add_task("Composing report", start=False)

                    progress.start_task(research_task)
                    research = self._run_agent(
                        thread_name="research",
                        agent_id=self.research_agent_id,
                        prompt=self._build_research_prompt(request),
                    )
                    progress.update(research_task, completed=100)

                    if not research:
                        return WorkflowResult(False, "Research phase failed", artifacts=self.artifacts)

                    progress.start_task(analysis_task)
                    analysis = self._run_agent(
                        thread_name="analysis",
                        agent_id=self.analysis_agent_id,
                        prompt=self._build_analysis_prompt(research),
                    )
                    progress.update(analysis_task, completed=100)

                    if not analysis:
                        return WorkflowResult(
                            False,
                            "Analysis phase failed",
                            research_content=research,
                            artifacts=self.artifacts,
                        )

                    progress.start_task(writing_task)
                    report = self._run_agent(
                        thread_name="writing",
                        agent_id=self.writing_agent_id,
                        prompt=self._build_writing_prompt(analysis, request.output_format),
                    )
                    progress.update(writing_task, completed=100)

                    if not report:
                        return WorkflowResult(
                            False,
                            "Writing phase failed",
                            research_content=research,
                            analysis_content=analysis,
                            artifacts=self.artifacts,
                        )

                    path = Path("connected_agents_report.md")
                    path.write_text(report, encoding="utf-8")
                    self.artifacts.report_path = path

                    return WorkflowResult(
                        True,
                        "Workflow completed",
                        research_content=research,
                        analysis_content=analysis,
                        final_report=report,
                        artifacts=self.artifacts,
                    )

        except Exception as exc:  # pragma: no cover - demo scenario
            return WorkflowResult(False, f"Unexpected error: {exc}", artifacts=self.artifacts)
        finally:
            self.client = None

    def _run_agent(self, thread_name: str, agent_id: str, prompt: str) -> Optional[str]:
        if not hasattr(self, "client") or self.client is None:
            raise RuntimeError("Client is not initialized")
        thread = self.client.agents.threads.create()
        setattr(self.artifacts, f"{thread_name}_thread", thread.id)

        self.client.agents.messages.create(thread_id=thread.id, role="user", content=prompt)
        run = self.client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent_id)

        if run.status != "completed":
            console.log(f"Run failed for {thread_name}: {run.last_error}")
            return None

        messages = list(self.client.agents.messages.list(thread.id, order="desc", limit=1))
        if messages and messages[0].role == "assistant":
            return messages[0].content[0].text.value
        return None

    @staticmethod
    def _build_research_prompt(request: ResearchRequest) -> str:
        return textwrap.dedent(
            f"""
            You are a research specialist. Investigate the topic below and return structured JSON.

            Topic: {request.topic}
            Scope: {request.scope}
            Time period: {request.time_period or "recent developments"}
            Language: {request.language}
            Depth: {request.depth}
            Minimum sources: {request.sources_required}

            Return a JSON object with keys: summary, sources (list with title/url/insight),
            statistics, viewpoints, gaps.
            """
        ).strip()

    @staticmethod
    def _build_analysis_prompt(research_content: str) -> str:
        return textwrap.dedent(
            f"""
            You are an analysis specialist. You will receive JSON from the research agent.
            Produce a JSON object containing:
            - themes (list)
            - strengths
            - weaknesses
            - contradictions
            - implications
            - recommendations

            Research JSON:
            {research_content}
            """
        ).strip()

    @staticmethod
    def _build_writing_prompt(analysis_content: str, format_name: str) -> str:
        format_hints = {
            "business_report": "Executive summary, key findings, recommendations",
            "academic_paper": "Abstract, introduction, methodology, results, conclusion",
            "blog_post": "Hook, narrative flow, key takeaways, call to action",
        }
        hint = format_hints.get(format_name, format_hints["business_report"])
        return textwrap.dedent(
            f"""
            You are a writing specialist. Create a polished document using the structure:
            {hint}

            Analysis JSON:
            {analysis_content}
            """
        ).strip()


def _render_summary(result: WorkflowResult) -> None:
    table = Table(title="Connected Agents workflow summary", show_lines=True)
    table.add_column("Phase")
    table.add_column("Status")
    table.add_column("Thread ID")

    table.add_row("Research", "✅" if result.research_content else "❌", result.artifacts.research_thread or "-")
    table.add_row("Analysis", "✅" if result.analysis_content else "❌", result.artifacts.analysis_thread or "-")
    table.add_row("Writing", "✅" if result.final_report else "❌", result.artifacts.writing_thread or "-")

    console.print(table)

    if result.artifacts.report_path:
        console.print(f"[bold green]Report saved to[/]: {result.artifacts.report_path}")


@app.command(help="Run the full multi-agent workflow")
def run(
    topic: str = typer.Option(..., prompt=True, help="Research topic"),
    sources: int = typer.Option(5, min=1, max=12, help="Minimum number of sources"),
    depth: str = typer.Option("moderate", help="Research depth"),
    output: str = typer.Option("business_report", help="Output format"),
) -> None:
    request = ResearchRequest(topic=topic, sources_required=sources, depth=depth, output_format=output)
    orchestrator = ConnectedAgentsOrchestrator()

    result = orchestrator.run(request)
    _render_summary(result)

    if result.final_report:
        console.print(Panel(result.final_report, title="Final report", expand=False))
    else:
        console.print(f"[red]{result.message}[/red]")


@app.command(help="Show currently configured agent IDs")
def info() -> None:
    orchestrator = ConnectedAgentsOrchestrator()
    table = Table(title="Connected agents configuration")
    table.add_column("Role")
    table.add_column("Agent ID")
    table.add_row("Research", orchestrator.research_agent_id)
    table.add_row("Analysis", orchestrator.analysis_agent_id)
    table.add_row("Writing", orchestrator.writing_agent_id)
    console.print(table)


def main() -> None:
    app()


if __name__ == "__main__":
    main()