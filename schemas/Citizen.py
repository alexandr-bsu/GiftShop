from pydantic import BaseModel, PositiveInt
from typing import Literal, List
from schemas._types import DMYPointPastDate, NotEmptyStr

class Citizen(BaseModel):
    citizen_id: PositiveInt
    town: NotEmptyStr
    street: NotEmptyStr
    building: NotEmptyStr
    apartment: PositiveInt
    name: NotEmptyStr
    birth_date: DMYPointPastDate
    gender: Literal['male', 'female']
    relatives: List[PositiveInt]
