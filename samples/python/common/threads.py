from __future__ import annotations

import logging
from typing import Iterable

from azure.ai.agents.models import MessageRole

_logger = logging.getLogger(__name__)


def pretty_print_messages(messages: Iterable) -> None:
    """Log agent thread messages in chronological order."""

    for message in messages:
        role = getattr(message, "role", "unknown")
        if isinstance(role, MessageRole):
            role = role.value
        text_items = []
        for content in getattr(message, "text_messages", []):
            text_items.append(content.text.value)
        if not text_items and hasattr(message, "content"):
            # Fallback for REST-shaped responses
            text_items.append(str(getattr(message, "content")))

        for line in text_items:
            _logger.info("%s: %s", role, line)
