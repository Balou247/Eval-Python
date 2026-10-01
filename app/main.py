from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import IntegrityError

DATABASE_URL = "sqlite:///./stations.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

class StationDB(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

class StationCreate(BaseModel):
    code: str = Field(min_length=1)
    name: str = Field(min_length=1)
    capacity: int = Field(ge=1)
    status: Literal["open", "closed", "maintenance"] = "open"

class StationPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    status: Literal["open", "closed", "maintenance"] | None = None

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def station_to_dict(station):
    return {
        "id": station.id,
        "code": station.code,
        "name": station.name,
        "capacity": station.capacity,
        "status": station.status
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/stations", status_code=201)
def create_station(data: StationCreate, db: Session = Depends(get_db)):
    station = StationDB(
        code=data.code,
        name=data.name,
        capacity=data.capacity,
        status=data.status
    )

    db.add(station)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Code déjà utilisé")

    db.refresh(station)
    return station_to_dict(station)

@app.get("/stations")
def get_stations(
    status: Literal["open", "closed", "maintenance"] | None = None,
    db: Session = Depends(get_db)
):
    if status is None:
        stations = db.query(StationDB).all()
    else:
        stations = db.query(StationDB).filter(StationDB.status == status).all()

    resultat = []

    for station in stations:
        resultat.append(station_to_dict(station))

    return resultat

@app.get("/stations/{station_id}")
def get_station(station_id: int, db: Session = Depends(get_db)):
    station = db.query(StationDB).filter(StationDB.id == station_id).first()

    if station is None:
        raise HTTPException(status_code=404, detail="Station introuvable")

    return station_to_dict(station)

@app.patch("/stations/{station_id}")
def update_station(
    station_id: int,
    data: StationPatch,
    db: Session = Depends(get_db)
):
    station = db.query(StationDB).filter(StationDB.id == station_id).first()

    if station is None:
        raise HTTPException(status_code=404, detail="Station introuvable")

    if data.name is not None:
        station.name = data.name

    if data.status is not None:
        station.status = data.status

    db.commit()
    db.refresh(station)

    return station_to_dict(station)
