from pydantic import BaseModel
from datetime import datetime
from typing import List


class Doc(BaseModel):
    BaseId: int
    Mark: str
    expdate: datetime


class Package(BaseModel):
    items: List[Doc]
