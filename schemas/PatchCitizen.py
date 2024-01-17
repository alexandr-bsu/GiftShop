from pydantic import BaseModel, PositiveInt
from typing import Literal, List
from schemas._types import DMYPointPastDate, NotEmptyStr

class PatchCitizen(BaseModel):
    town: NotEmptyStr = None
    street: NotEmptyStr = None
    building: NotEmptyStr = None
    apartment: PositiveInt = None
    name: NotEmptyStr = None
    birth_date: DMYPointPastDate = None
    gender: Literal['male', 'female'] = None
    relatives: List[PositiveInt] = None