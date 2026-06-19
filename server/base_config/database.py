from urllib.parse import quote_plus
import os

print(f"DB_USERNAME: {os.getenv('DB_USERNAME')}")

DataBaseConfig = {
    "db_username": os.getenv("DB_USERNAME"),
    "db_password": os.getenv("DB_PASSWORD"),
    "db_host": os.getenv("DB_HOST"),
    "db_port": os.getenv("DB_PORT"),
    "db_database": os.getenv("DB_NAME"),
}


def build_sync_sqlalchemy_database_url() -> str:
    """
    构建同步 SQLAlchemy 数据库连接 URL

    :return: 同步 SQLAlchemy 数据库连接 URL
    """
    return (
        f"postgresql+psycopg://{DataBaseConfig['db_username']}:{quote_plus(DataBaseConfig['db_password'])}@"
        f"{DataBaseConfig['db_host']}:{DataBaseConfig['db_port']}/{DataBaseConfig['db_database']}"
    )


SYNC_SQLALCHEMY_DATABASE_URL = build_sync_sqlalchemy_database_url()
