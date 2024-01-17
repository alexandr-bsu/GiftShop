from schemas.ImportCitizens import ImportCitizens
from schemas.utils import extract_citizen_birth_date_to_dict
from .utils import (get_last_id,
                    get_citizen_by_import_id_citizen_id,
                    gen_model_update_placeholder,
                    exclude_intersection,
                    get_gifts_by_import_id_and_month,
                    get_ages_town_by_import_id)
from Exceptions import BusinessLogicException
import asyncpg
from numpy import percentile
from settings import DB_SETTINGS
async def connect():
    return await asyncpg.connect(**DB_SETTINGS)


async def import_citizens(citizens: ImportCitizens):
    conn = await connect()
    citizens_birth_dates = extract_citizen_birth_date_to_dict(citizens)
    import_id = await get_last_id(conn, 'Citizens', 'import_id')

    if import_id is None:
        import_id = 1
    else:
        import_id += 1

    for citizen in citizens.citizens:
        await conn.execute('INSERT INTO Citizens '
                           '(import_id, citizen_id, town, street, building, apartment, name, birth_date, gender) '
                           'VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9)',
                           import_id, citizen.citizen_id, citizen.town, citizen.street, citizen.building,
                           citizen.apartment, citizen.name, citizen.birth_date, citizen.gender)

        for relative in citizen.relatives:
            await conn.execute('INSERT INTO Relations(import_id, citizen_id, relative_id, relative_birth_date) '
                               'VALUES($1, $2, $3, $4)',
                               import_id, citizen.citizen_id, relative, citizens_birth_dates[relative])

    return import_id


async def update_citizen_by_import_id_citizen_id(citizen, import_id, citizen_id):
    conn = await connect()
    citizen_from_db = await get_citizen_by_import_id_citizen_id(conn, import_id, citizen_id)
    if citizen_from_db is None:
        raise BusinessLogicException('No such user')

    update_placeholder, values = gen_model_update_placeholder(citizen)
    query = (f'UPDATE Citizens SET {update_placeholder} '
             f'WHERE import_id=${len(values) + 1} AND citizen_id=${len(values) + 2} ')

    # Create transaction to rollback in case of error
    async with conn.transaction():
        # If we get fields for update
        if len(values) != 0:
            await conn.execute(query, *values, import_id, citizen_id)
        elif len(values) == 0 and citizen.relatives is None:
            raise BusinessLogicException('Nothing to update')

        # Update citizen birth_date in Relations
        if citizen.birth_date is not None:
            await conn.execute('UPDATE Relations SET relative_birth_date=$1 WHERE relative_id=$2',
                           citizen.birth_date, citizen_id)

        if citizen.relatives is not None:
            if citizen.birth_date is not None:
                citizen_birth_date = citizen.birth_date
            else:
                citizen_birth_date = citizen_from_db['birth_date']

            citizen_relatives_set = set(citizen.relatives)
            citizen_relatives_db = citizen_from_db['relatives']

            # Transform db citizen_relative answer into set for efficient fast check for an instance
            if citizen_relatives_db is not None:
                citizen_relatives_db = set(citizen_relatives_db)
            else:
                citizen_relatives_db = set()

            # Avoid updates for relations which intersect (db and query)
            citizen_relatives_set, citizen_relatives_db = exclude_intersection(citizen_relatives_set, citizen_relatives_db)

            for relative_id in citizen_relatives_set:
                # If relative relation already in db, we don't need to do anything
                if relative_id not in citizen_relatives_db:
                    if relative_id == citizen_id:
                        raise BusinessLogicException('Citizen can\'t be relative to self')

                    relative_from_db = await get_citizen_by_import_id_citizen_id(conn, import_id, relative_id)
                    if relative_from_db is None:
                        raise BusinessLogicException('No such user in DB')

                    # add relationship to db
                    await conn.execute('INSERT INTO Relations (import_id, citizen_id, relative_id, relative_birth_date)'
                                       'VALUES ($1, $2, $3, $4), ($1, $3, $2, $5)',
                                       import_id, citizen_id, relative_id, relative_from_db['birth_date'],
                                       citizen_birth_date)

            # Delete relations if they not in Query
            for relative_id_to_delete in citizen_relatives_db:
                if relative_id_to_delete not in citizen_relatives_set:
                    await conn.execute('DELETE FROM Relations WHERE import_id=$1 AND citizen_id=$2 AND relative_id=$3 ',
                                       import_id, citizen_id, relative_id_to_delete)
                    await conn.execute('DELETE FROM Relations WHERE import_id=$1 AND citizen_id=$2 AND relative_id=$3 ',
                                       import_id, relative_id_to_delete, citizen_id)

    return {"data": await get_citizen_by_import_id_citizen_id(conn, import_id, citizen_id)}


async def list_users_by_import_id(import_id):
    conn = await connect()
    return {"data": await conn.fetch(
        'SELECT Citizens.*, array_agg(Relations.relative_id) as relatives FROM Citizens LEFT JOIN Relations '
        'ON Relations.citizen_id = Citizens.citizen_id AND Relations.import_id = Citizens.import_id '
        'WHERE Citizens.import_id=$1 '
        'GROUP BY citizens.id, Citizens.import_id, Citizens.citizen_id',
        import_id
    )}


async def count_gifts_in_months_by_import_id(import_id):
    conn = await connect()
    birth_dates = {month: await get_gifts_by_import_id_and_month(conn, import_id, month) for month in range(1, 13)}
    return {"data": birth_dates}


async def get_stat_age_town_percentile_by_import_id(import_id):
    conn = await connect()
    ages_by_town = await get_ages_town_by_import_id(conn, import_id)
    stat_by_percentile = [{'town': town_item['town'],
                           'p50': percentile(town_item['ages'], 50),
                           'p75': percentile(town_item['ages'], 75),
                           'p99': percentile(town_item['ages'], 99),
                           } for town_item in ages_by_town]
    return {"data": stat_by_percentile}
