from dataclasses import dataclass, asdict, field
from typing import List, Optional, Union

@dataclass
class StreamItem:
    title: str
    type: str = "pelicula"
    year: Optional[str] = None
    poster: Optional[str] = None
    stream: Optional[str] = None
    seasons: Optional[str] = None
    alt_streams: List[str] = field(default_factory=list)
    genre: Optional[str] = None
    rating: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None
    cast: Optional[str] = None
    director: Optional[str] = None
    backdrop: Optional[str] = None
    trailer: Optional[str] = None
    event_date: Optional[str] = None
    event_status: Optional[str] = None
    source: str = ""

    def to_dict(self):
        d = asdict(self)
        return {k: v for k, v in d.items() if v not in [None, []]}
