from urllib.parse import quote_plus

DataBaseConfig = {
    "db_username": "postgres",
    "db_password": "postgres",
    "db_host": "127.0.0.1",
    "db_port": 5432,
    "db_database": "documents_center",
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
