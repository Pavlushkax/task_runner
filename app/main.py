from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from app.database import engine, Base, SessionLocal
from app.models import Job
from app.celery_app import run_job_task

# FastAPI uygulamasını oluşturuyoruz
app = FastAPI(title="Task Runner API", description="Arka plan görevlerini yöneten RESTful API")

# Uygulama başlarken veritabanı tablolarını otomatik oluşturur (Eğer yoksa)
Base.metadata.create_all(bind=engine)

# Veritabanı oturumu almak için Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API'ye veri gönderirken kullanılacak Pydantic şeması (Veri doğrulama)
class JobCreate(BaseModel):
    job_type: str  # "os_command" veya "katana" vb.
    payload: str   # çalıştırılacak komut veya url

class JobResponse(BaseModel):
    id: int
    job_type: str
    status: str
    payload: str
    result: str | None = None

    class Config:
        orm_mode = True

@app.post("/jobs", response_model=JobResponse, status_code=201)
def create_job(job_in: JobCreate, db: Session = Depends(get_db)):
    """
    Sisteme yeni bir iş (job) ekler ve arka planda çalışmasını tetikler.
    """
    # 1. Veritabanına yeni job'u "pending" olarak kaydet
    new_job = Job(
        job_type=job_in.job_type,
        payload=job_in.payload,
        status="pending"
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    # 2. Celery ile arka plan görevini tetikle
    run_job_task.delay(new_job.id)

    return new_job

@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    ID'si verilen job'un durumunu ve eğer bittiyse sonucunu döner.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job bulunamadı")
    return job

@app.get("/jobs", response_model=List[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    """
    Sistemdeki tüm job'ları listeler.
    """
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    return jobs
