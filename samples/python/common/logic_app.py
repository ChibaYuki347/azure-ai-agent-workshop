from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from typing import Callable

import requests
from azure.ai.projects.models import FunctionTool

_logger = logging.getLogger(__name__)


@dataclass(slots=True)
class LogicAppToolConfig:
    callback_url: str


def create_logic_app_function_tool(config: LogicAppToolConfig) -> FunctionTool:
    """Create a function tool that forwards agent tool calls to a Logic App.

    The generated tool expects the agent to provide ``to``, ``subject``, and ``body`` fields.
    The Logic App is triggered via HTTP POST with a JSON payload.
    """

    def send_email_via_logic_app(to: str, subject: str, body: str) -> str:
        """Send an email via the configured Logic App workflow.

        Parameters
        ----------
        to: str
            Recipient email address.
        subject: str
            Subject line for the message.
        body: str
            Body text for the message.
        """

        payload = {"to": to, "subject": subject, "body": body}
        _logger.debug(
            "Payload for Logic App request: %s (Logic App へ送信するペイロード)", payload
        )
        response = requests.post(config.callback_url, json=payload, timeout=30)
        response.raise_for_status()
        return json.dumps({"status": response.status_code, "location": response.headers.get("Location")})

    send_email_via_logic_app.__name__ = "send_email_via_logic_app"
    send_email_via_logic_app.__doc__ = (
        "Send an email using a Logic App trigger. Parameters must include to, subject, and body."
    )

    return FunctionTool(functions={send_email_via_logic_app})
