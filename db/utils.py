async def get_last_id(conn, table, id_column):
    last_id = await conn.fetchrow(f'SELECT {id_column} FROM {table} ORDER BY {id_column} DESC LIMIT 1')
    if last_id is None:
        return 0
    else:
        return last_id[id_column]


async def get_citizen_by_import_id_citizen_id(conn, import_id, citizen_id):
    # return await conn.fetchrow('SELECT Distinct(Citizens.*),'
    #                            'ARRAY(SELECT DISTINCT(relative_id) '
    #                            'FROM Relations '
    #                            'WHERE import_id=Citizens.import_id AND citizen_id=Citizens.citizen_id)'
    #                            'as relatives '
    #                            'FROM Citizens WHERE citizen_id = $2 AND import_id = $1',
    #                            import_id, citizen_id)

    return await conn.fetchrow(
        'SELECT Citizens.*, array_agg(Relations.relative_id) as relatives FROM Citizens LEFT JOIN Relations '
        'ON Relations.citizen_id = Citizens.citizen_id AND Relations.import_id = Citizens.import_id '
        'WHERE Citizens.import_id=$1 AND Citizens.citizen_id=$2 '
        'GROUP BY citizens.id, Citizens.import_id, Citizens.citizen_id',
        import_id, citizen_id
    )


async def get_citizen_relatives_by_import_id_citizen_id(conn, import_id, citizen_id):
    return await conn.fetchrow('SELECT relative_id FROM Relations WHERE import_id=$1 AND citizen_id=$2',
                               import_id, citizen_id)

def gen_model_update_placeholder(model):
    update_fields = model.model_dump(exclude_unset=True, exclude={'relatives'})
    return ','.join([f'{key}=${i + 1}' for i, key in enumerate(update_fields.keys())]), update_fields.values()

async def get_gifts_by_import_id_and_month(conn, import_id, month):
    return await conn.fetch("SELECT citizen_id, COUNT(*) as presents FROM Relations WHERE import_id=$1 "
                            "AND date_part('month', relative_birth_date) = $2 "
                            "GROUP BY citizen_id"
                            , import_id, month)

async def get_ages_town_by_import_id(conn, import_id):
    return await conn.fetch('SELECT town, array_agg(date_part(\'year\',age(birth_date))) as ages '
                            'FROM Citizens WHERE import_id=$1 '
                            'GROUP BY town', import_id)
def exclude_intersection(a, b):
    return a.difference(a & b), b.difference(a & b)
