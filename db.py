# db.py
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from models.db_models import ResumeSession, AgentOutput
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DB_URL, pool_pre_ping=True)

inspector = inspect(engine)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def check_db_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError:
        return False


def get_table_names():
    return inspector.get_table_names()


# FastAPI-compatible DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_resume_session_data():
    db = SessionLocal()
    # Query all ResumeSession rows
    sessions = db.query(ResumeSession).all()
    for s in sessions:
        print(f"Id is: {s.id}")
        print(f"Id with hash: {s.id} -- {s.hash}")
        print(f"Id with Resume: {s.id} -- {s.resume[:100]}")
        print(f"Id with JD: {s.id} -- {s.job_description[:100]}")
        print("***" * 10)


def get_agent_output_data():
    db = SessionLocal()
    # Query all AgentOutput rows
    outputs = db.query(AgentOutput).all()
    for o in outputs:
        print(f"Agent name: {o.agent_name}")
        print(f"Created at: {o.created_at}")
        print(f"Output: {o.output}")
        print("***" * 10)


if __name__ == "__main__":
    # print(get_table_names())

    get_resume_session_data()

    print("^^^^^^^^^" * 10)

    get_agent_output_data()
