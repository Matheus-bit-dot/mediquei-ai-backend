from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///mediquei_leads.db")
Base = declarative_base()

class Lead(Base):
    __tablename__ = 'leads'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    whatsapp = Column(String)
    interesse = Column(String)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)