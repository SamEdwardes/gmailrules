import datetime as dt
from typing import Optional, Dict, List

from rich import print, inspect

from pydantic import BaseModel, Field, validator


class AppProperty(BaseModel):
    name: str = Field(alias="@name")
    value: str = Field(alias="@value")


class AppPropertyTidy(BaseModel):
    email: Optional[str] = Field(alias="from")
    label: Optional[str]
    should_archive: Optional[str]


class Entry(BaseModel):
    category: Dict[str, str]
    id: str
    updated: dt.datetime
    content: Optional[str]
    apps_property: Optional[List[AppProperty]] = Field(alias="apps:property")
    apps_property_tidy: Optional[List[AppPropertyTidy]]

    @validator('apps_property_tidy')
    def populate_apps_property_tidy(cls, v):
        print("VALIDING MODEL")
        out = []
        for app_property in cls.apps_property:
            print(app_property)
            app_property_tidy = AppPropertyTidy()
            if app_property.name == "from":
                app_property_tidy.email = app_property.value
            elif app_property.name == "label":
                app_property_tidy.label = app_property.value
            elif app_property.name == "shouldArchive":
                app_property_tidy.should_archive = app_property.value
            out.append(app_property_tidy)
        print(out)
        return out


class Feed(BaseModel):
    title: str
    id: str
    updated: dt.datetime
    author: Dict[str, str]
    entry: List[Entry]


class RuleSet(BaseModel):
    feed: Feed


class Action(BaseModel):
    """A model to capture a summarized version of the rules from gmail."""
    label: str
    emails: List[str]
    should_archive: bool