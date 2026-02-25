from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False, unique=True)
    release_date = Column(String)
    display_size = Column(Float)
    battery_mAh = Column(Integer)   # matches JSON
    camera_mp = Column(String)      # matches JSON
    base_ram_gb = Column(Integer)   # matches JSON
    storage_options = Column(String)
    price_usd = Column(Float)          # matches JSON

engine = create_engine("postgresql://postgres:123456789@localhost:5432/samsung_db")
Base.metadata.create_all(engine)