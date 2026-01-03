# sabse pehle hamne yaha SQLAlchemy ORM ke tools import kiye hain
# create_engine → database connection banane ke liye use hota hai
from sqlalchemy import create_engine

# sessionmaker → database session banane ke liye
# declarative_base → sabhi ORM models ka base class
from sqlalchemy.orm import sessionmaker, declarative_base

# yaha MySQL database ka connection URL diya gaya hai
# format: mysql+pymysql://username:password@host:port/database_name
# password "Mysql@2025#" ko URL encode karke "Mysql%402025%23" likha gaya hai
DATABASE_URL = "mysql+pymysql://root:Mysql%402025%23@localhost:3306/secure_notes_fastapi"

# create_engine ka use karke MySQL database se connection bana rahe hain
engine = create_engine(
    DATABASE_URL,
    echo=False  # SQL queries terminal me ni dikhengi (debug ke liye)
)

# SessionLocal se hume database session milta hai
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Base ek base class hai
# hamare sabhi ORM models (User, Note) isi Base se inherit karte hain
Base = declarative_base()
