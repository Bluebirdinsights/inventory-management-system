from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables
load_dotenv()

# Database URL with correct port
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=0,
    connect_args={
        'sslmode': 'require',  # Adding SSL mode for Aiven
        'connect_timeout': 10  # Adding connection timeout
    }
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@st.cache_resource
def get_engine():
    return engine

def init_db():
    """Initialize database connection in Streamlit session state"""
    if 'db' not in st.session_state:
        st.session_state.db = SessionLocal()

def get_db():
    """Get database session"""
    if 'db' not in st.session_state:
        init_db()
    return st.session_state.db