from pydantic import BaseModel, model_validator
from .Citizen import Citizen
from schemas.validators import check_citizen_unique, check_not_relative_to_self, check_are_relations_symmetric
from schemas.utils import difference_relatives
from typing import List


class ImportCitizens(BaseModel):
    citizens: List[Citizen]

    # Validator should be super-function to support validation context
    @model_validator(mode='after')
    def validator(cls, data):
        citizens = data.citizens
        citizens_relatives = {}

        for citizen in citizens:
            # Check: All citizen_id in batch are unique
            check_citizen_unique(citizen, citizens_relatives)

            # Add sets of relatives to dict for fast access
            citizens_relatives[citizen.citizen_id] = set(citizen.relatives)

            # Check: Citizen not relative to himself/herself
            check_not_relative_to_self(citizen, citizens_relatives)

            # If relations are symmetric, all sets of citizens relatives will be empty
            difference_relatives(citizen, citizens_relatives)

        # Check: All relations are symmetric
        check_are_relations_symmetric(citizens_relatives)
        return data
