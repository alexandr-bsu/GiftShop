from fastapi.routing import APIRouter
from schemas import ImportCitizens, PatchCitizen
import db.actions as db_acts

router = APIRouter(prefix='/imports')

@router.post('/', status_code=201)
async def import_citizens(citizens: ImportCitizens.ImportCitizens):
    import_id = await db_acts.import_citizens(citizens)
    return {'data': {'import_id': import_id}}


@router.patch('/{import_id:int}/citizens/{citizen_id:int}')
async def change_citizen(citizen_info: PatchCitizen.PatchCitizen, import_id: int, citizen_id: int):
    return await db_acts.update_citizen_by_import_id_citizen_id(citizen_info, import_id, citizen_id)


@router.get('/{import_id:int}/citizens')
async def list_citizens(import_id: int):
    return await db_acts.list_users_by_import_id(import_id)


@router.get('/{import_id:int}/citizens/birthdays')
async def get_presents_grouped_by_birthday(import_id):
    return await db_acts.count_gifts_in_months_by_import_id(import_id)


@router.get('/{import_id:int}/towns/stat/percentile/age')
async def get_age_percentile_grouped_by_town(import_id):
    return await db_acts.get_stat_age_town_percentile_by_import_id(import_id)
