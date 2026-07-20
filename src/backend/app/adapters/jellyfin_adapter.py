"""JellyfinAdapter for library listing and content metadata."""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

TICKS_PER_MS = 10_000

ITEM_FIELDS = (
    "Genres,ProviderIds,Overview,OfficialRating,CommunityRating,"
    "CriticRating,Studios,People,RunTimeTicks,ProductionYear"
)


class JellyfinAdapter:
    """Adapter for Jellyfin API interactions."""

    def __init__(self, base_url: str, api_key: str, timeout: float = 30.0) -> None:
        """
        Initialize Jellyfin adapter.

        Args:
            base_url: Jellyfin server URL
            api_key: Jellyfin API key
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._client: httpx.Client | None = None

    def _get_client(self) -> httpx.Client:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers={
                    "Authorization": f'MediaBrowser Token="{self.api_key}"',
                },
                timeout=self.timeout,
            )
        return self._client

    def test_connection(self) -> tuple[bool, str]:
        """
        Test connection to Jellyfin.

        Returns:
            (success, message)
        """
        try:
            client = self._get_client()
            response = client.get("/System/Info")
            if response.status_code == 401:
                return False, "Invalid Jellyfin API key"
            response.raise_for_status()
            data = response.json()
            name = data.get("ServerName", "Jellyfin")
            version = data.get("Version", "")
            return True, f"Connected to {name} (Jellyfin {version})".rstrip()
        except httpx.HTTPStatusError as e:
            return False, f"Connection error: HTTP {e.response.status_code}"
        except Exception as e:
            return False, f"Connection error: {str(e)}"

    def get_libraries(self) -> list[dict[str, Any]]:
        """Get all libraries from Jellyfin."""
        client = self._get_client()
        response = client.get("/Library/VirtualFolders")
        response.raise_for_status()

        # Map Jellyfin collection types to library types used internally
        type_map = {"movies": "movie", "tvshows": "show"}

        libraries = []
        for folder in response.json():
            library_id = folder.get("ItemId", "")
            collection_type = folder.get("CollectionType", "")
            count_response = client.get(
                "/Items",
                params={
                    "ParentId": library_id,
                    "Recursive": "true",
                    "IncludeItemTypes": "Movie,Episode",
                    "Limit": 0,
                },
            )
            total_items = 0
            if count_response.status_code == 200:
                total_items = count_response.json().get("TotalRecordCount", 0)

            libraries.append(
                {
                    "id": library_id,
                    "title": folder.get("Name", ""),
                    "type": type_map.get(collection_type, collection_type),
                    "uuid": library_id,
                    "total_items": total_items,
                }
            )

        return libraries

    def get_library_content(
        self,
        library_id: str,
        content_type: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get content from a library.

        Args:
            library_id: Library ID
            content_type: Filter by type (movie, episode)
            limit: Maximum items to return

        Returns:
            List of content items
        """
        client = self._get_client()

        type_map = {"movie": "Movie", "episode": "Episode", "show": "Series"}
        include_types = type_map.get(content_type or "", "Movie,Episode")

        params: dict[str, Any] = {
            "ParentId": library_id,
            "Recursive": "true",
            "IncludeItemTypes": include_types,
            "Fields": ITEM_FIELDS,
        }
        if limit:
            params["Limit"] = limit

        response = client.get("/Items", params=params)
        if response.status_code == 404:
            logger.warning(f"Library {library_id} not found")
            return []
        response.raise_for_status()

        return [
            self._item_to_dict(item, library_id)
            for item in response.json().get("Items", [])
        ]

    def _item_to_dict(self, item: dict[str, Any], library_id: str) -> dict[str, Any]:
        """Convert Jellyfin item to dictionary."""
        item_type = item.get("Type", "").lower()  # movie/episode/series
        if item_type == "series":
            item_type = "show"

        duration_ms = (item.get("RunTimeTicks") or 0) // TICKS_PER_MS

        base = {
            "jellyfin_id": item.get("Id", ""),
            "title": item.get("Name", ""),
            "type": item_type,
            "duration_ms": duration_ms,
            "year": item.get("ProductionYear"),
            "library_id": library_id,
            "genres": item.get("Genres", []),
            "content_rating": item.get("OfficialRating"),
            "rating": item.get("CriticRating"),
            "audience_rating": item.get("CommunityRating"),
        }

        if item_type == "episode":
            show_title = item.get("SeriesName", "")
            season = item.get("ParentIndexNumber") or 0
            episode = item.get("IndexNumber") or 0
            base["show_title"] = show_title
            base["season_number"] = season
            base["episode_number"] = episode
            base["title"] = f"{show_title} - S{season:02d}E{episode:02d} - {item.get('Name', '')}"
            # Episodes often have no genres - fall back to series genres
            if not base["genres"] and item.get("SeriesId"):
                try:
                    series = self._fetch_item(item["SeriesId"])
                    if series:
                        base["genres"] = series.get("Genres", [])
                except Exception:
                    pass

        base["rating_key"] = item.get("Id", "")

        return base

    def _fetch_item(self, item_id: str) -> dict[str, Any] | None:
        """Fetch a single item by ID."""
        client = self._get_client()
        response = client.get(
            "/Items",
            params={"Ids": item_id, "Fields": ITEM_FIELDS, "Recursive": "true"},
        )
        if response.status_code != 200:
            return None
        items = response.json().get("Items", [])
        return items[0] if items else None

    def get_content_metadata(self, jellyfin_id: str) -> dict[str, Any] | None:
        """
        Get detailed metadata for a content item.

        Args:
            jellyfin_id: Jellyfin item ID

        Returns:
            Metadata dictionary or None if not found
        """
        item = self._fetch_item(jellyfin_id)
        if item is None:
            return None

        item_type = item.get("Type", "").lower()
        if item_type == "series":
            item_type = "show"

        people = item.get("People", [])
        directors = [p.get("Name", "") for p in people if p.get("Type") == "Director"]
        actors = [p.get("Name", "") for p in people if p.get("Type") == "Actor"][:10]
        studios = item.get("Studios", [])

        metadata = {
            "jellyfin_id": item.get("Id", ""),
            "title": item.get("Name", ""),
            "type": item_type,
            "duration_ms": (item.get("RunTimeTicks") or 0) // TICKS_PER_MS,
            "year": item.get("ProductionYear"),
            "genres": item.get("Genres", []),
            "directors": directors,
            "actors": actors,
            "studio": studios[0].get("Name") if studios else None,
            "content_rating": item.get("OfficialRating"),
            "summary": item.get("Overview"),
            "rating": item.get("CriticRating"),
            "audience_rating": item.get("CommunityRating"),
        }

        provider_ids = item.get("ProviderIds", {})
        for key, value in provider_ids.items():
            if key.lower() == "tmdb":
                metadata["tmdb_id"] = value
            elif key.lower() == "imdb":
                metadata["imdb_id"] = value

        return metadata

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
            library_id: Optional library to search in
            limit: Maximum results

        Returns:
            List of matching items
        """
        client = self._get_client()

        params: dict[str, Any] = {
            "SearchTerm": query,
            "Recursive": "true",
            "IncludeItemTypes": "Movie,Series,Episode",
            "Fields": ITEM_FIELDS,
            "Limit": limit,
        }
        if library_id:
            params["ParentId"] = library_id

        response = client.get("/Items", params=params)
        response.raise_for_status()

        return [
            self._item_to_dict(item, library_id or "0")
            for item in response.json().get("Items", [])
        ]
