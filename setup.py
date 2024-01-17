import asyncpg
import asyncio
from settings import DB_SETTINGS
async def connect():
    return await asyncpg.connect(**DB_SETTINGS)

SQL_QUERY = """
CREATE TABLE citizens (
    id SERIAL PRIMARY KEY NOT NULL,
    import_id BIGINT NOT NULL,
    citizen_id BIGINT NOT NULL,
    town VARCHAR NOT NULL,
    street VARCHAR NOT NULL,
    building VARCHAR NOT NULL,
    apartment BIGINT NOT NULL,
    name VARCHAR NOT NULL,
    birth_date DATE NOT NULL,
    gender VARCHAR NOT NULL
);

CREATE TABLE relations(
    import_id BIGINT NOT NULL,
    citizen_id BIGINT NOT NULL,
    relative_id BIGINT NOT NULL REFERENCES citizens,
    relative_birth_date DATE NOT NULL 
)
"""

async def main(sql):
    conn = await connect()
    await conn.execute(sql)

if __name__ == '__main__':
    asyncio.run(main(SQL_QUERY))