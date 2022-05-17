import datetime as dt
from typing import Optional, Dict, List

from pydantic import BaseModel

class AppProperty(BaseModel):
    name: str

class Entry(BaseModel):
    category: str
    id: str
    updated: dt.datetime
    content: Optional[str]

class Feed(BaseModel):
    title: str
    id: str
    update: dt.datetime
    author: Dict[str, str]
    entry: List[Entry]

class RuleSet(BaseModel):
    xml: Dict[str, str]
    feed: Feed

