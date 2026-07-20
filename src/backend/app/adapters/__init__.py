"""External service adapters."""

from app.adapters.jellyfin_adapter import JellyfinAdapter
from app.adapters.tunarr_adapter import TunarrAdapter

__all__ = ["TunarrAdapter", "JellyfinAdapter"]
