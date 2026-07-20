"""JellyfinService with library listing and connection testing."""

import logging
from typing import Any

from app.adapters.jellyfin_adapter import JellyfinAdapter

logger = logging.getLogger(__name__)


class JellyfinService:
    """Service for Jellyfin interactions."""

    def __init__(self, url: str, api_key: str) -> None:
        """
        Initialize Jellyfin service.

        Args:
            url: Jellyfin server URL
            api_key: Jellyfin API key
        """
        self.adapter = JellyfinAdapter(url, api_key)

    def test_connection(self) -> tuple[bool, str]:
        """
        Test connection to Jellyfin server.

        Returns:
            (success, message) tuple
        """
        return self.adapter.test_connection()

    def get_libraries(self) -> list[dict[str, Any]]:
        """
        Get all libraries from Jellyfin.

        Returns:
            List of library dictionaries
        """
        return self.adapter.get_libraries()

    def get_library_content(
        self,
        library_id: str,
        content_type: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get content from a specific library.

        Args:
            library_id: Library ID
            content_type: Optional content type filter
            limit: Maximum items to return

        Returns:
            List of content items
        """
        return self.adapter.get_library_content(library_id, content_type, limit)

    def get_content_metadata(self, jellyfin_id: str) -> dict[str, Any] | None:
        """
        Get detailed metadata for a content item.

        Args:
            jellyfin_id: Jellyfin item ID

        Returns:
            Metadata dictionary or None
        """
        return self.adapter.get_content_metadata(jellyfin_id)

    def search(
        self,
        query: str,
        library_id: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """
        Search for content.

        Args:
            query: Search query
            library_id: Optional library filter
            limit: Maximum results

        Returns:
            List of matching items
        """
        return self.adapter.search(query, library_id, limit)

    def get_server_info(self) -> dict[str, Any] | None:
        """
        Get Jellyfin server information.

        Returns:
            Server info dictionary or None on error
        """
        try:
            success, message = self.test_connection()
            if success:
                return {
                    "connected": True,
                    "server_name": message.replace("Connected to ", ""),
                    "libraries": self.get_libraries(),
                }
        except Exception as e:
            logger.error(f"Failed to get server info: {e}")

        return None
