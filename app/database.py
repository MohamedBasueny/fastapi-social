# import psycopg


# with psycopg.connect("dbname=fastapi host=localhost user=postgres password=0716103235") as conn:

#     # Open a cursor to perform database operations
#     with conn.cursor() as cur:
#         # Query the database and obtain data as Python objects.
#         cur.execute("SELECT * FROM posts")
#         cur.fetchone()
#         # will return (1, 100, "abc'def")

#         # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
#         # of several records, or even iterate on the cursor
#         for record in cur:
#             print(record)

#         # Make the changes to the database persistent
#         conn.commit()
############################################################# ORM ############################
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
from .config import settings
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:0716103235@localhost/fastapi"
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
