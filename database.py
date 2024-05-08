from tortoise import Tortoise
from dotenv import load_dotenv
import os

load_dotenv()


async def database_connection():
    await Tortoise.init(
        db_url=os.environ["DATABASE_POSTGRES_URL"], modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()
