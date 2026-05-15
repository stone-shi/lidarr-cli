import httpx
from typing import List, Dict, Any, Optional
from .config import settings
from .models import Artist, Album, SystemStatus, QueueItem, HistoryItem

class LidarrAPI:
    def __init__(self):
        self.base_url = f"{settings.lidarr_url.rstrip('/')}/api/v1"
        self.headers = {"X-Api-Key": settings.lidarr_api_key}
        self.client = httpx.Client(base_url=self.base_url, headers=self.headers)

    def get_system_status(self) -> SystemStatus:
        response = self.client.get("/system/status")
        response.raise_for_status()
        return SystemStatus(**response.json())

    def get_artists(self) -> List[Artist]:
        response = self.client.get("/artist")
        response.raise_for_status()
        return [Artist(**artist) for artist in response.json()]

    def search_artists(self, term: str) -> List[Artist]:
        response = self.client.get("/artist/lookup", params={"term": term})
        response.raise_for_status()
        return [Artist(**artist) for artist in response.json()]

    def get_albums(self, artist_id: Optional[int] = None) -> List[Album]:
        params = {}
        if artist_id:
            params["artistId"] = artist_id
        response = self.client.get("/album", params=params)
        response.raise_for_status()
        return [Album(**album) for album in response.json()]

    def post_command(self, name: str, **kwargs) -> Dict[str, Any]:
        payload = {"name": name, **kwargs}
        response = self.client.post("/command", json=payload)
        response.raise_for_status()
        return response.json()

    def get_queue(self, page: int = 1, page_size: int = 10) -> List[QueueItem]:
        params = {"page": page, "pageSize": page_size, "sortKey": "timeleft", "sortDirection": "ascending"}
        response = self.client.get("/queue", params=params)
        response.raise_for_status()
        data = response.json()
        records = data.get("records", []) if isinstance(data, dict) else data
        return [QueueItem(**item) for item in records]

    def get_history(self, page: int = 1, page_size: int = 10) -> List[HistoryItem]:
        params = {"page": page, "pageSize": page_size, "sortKey": "date", "sortDirection": "descending"}
        response = self.client.get("/history", params=params)
        response.raise_for_status()
        data = response.json()
        records = data.get("records", []) if isinstance(data, dict) else data
        return [HistoryItem(**item) for item in records]
