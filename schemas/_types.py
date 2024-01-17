from typing import Annotated
from datetime import datetime
from pydantic import BeforeValidator, PastDate, constr
from validators import point_date_validate

DMYPointDate = Annotated[datetime, BeforeValidator(point_date_validate)]
DMYPointPastDate = Annotated[PastDate, BeforeValidator(point_date_validate)]
NotEmptyStr = constr(min_length=1)
