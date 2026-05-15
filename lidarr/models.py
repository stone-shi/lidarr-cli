from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict

class Artist(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: Optional[int] = None
    artistName: Optional[str] = None
    status: Optional[str] = None
    monitored: Optional[bool] = None
    path: Optional[str] = None
    mbid: Optional[str] = None

class Album(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: Optional[int] = None
    title: Optional[str] = None
    artistId: Optional[int] = None
    monitored: Optional[bool] = None
    status: Optional[str] = None

class SystemStatus(BaseModel):
    model_config = ConfigDict(extra="ignore")
    version: Optional[str] = None
    osName: Optional[str] = None
    isMono: Optional[bool] = None
    isLinux: Optional[bool] = None

class QueueStatusMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    title: str
    messages: List[str]

class QueueItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int
    title: str
    status: str
    size: float
    sizeleft: float
    timeleft: Optional[str] = None
    trackedDownloadStatus: Optional[str] = None
    trackedDownloadState: Optional[str] = None
    statusMessages: List[QueueStatusMessage] = []

class HistoryItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: int
    sourceTitle: str
    eventType: str
    date: str
