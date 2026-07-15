import os
from celery import Celery
from app.database import SessionLocal
from app.models import Job

# Sisteme eklediğimiz iş sınıflarını (Job classes) import ediyoruz.
from app.jobs.os_command import OSCommandJob
from app.jobs.web_crawl import WebCrawlJob

# Redis bağlantı adresini ortam değişkenlerinden alıyoruz, yoksa varsayılanı kullanıyoruz.
# Docker-compose içinde ortam değişkenleri atanmıştı.
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "task_runner",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

# Fabrika (Factory) Mantığı:
# Yeni bir job eklemek istediğinizde sınıfını import edip bu sözlüğe eklemeniz yeterlidir.
JOB_CLASSES = {
    "os_command": OSCommandJob,
    "katana": WebCrawlJob
}

@celery_app.task(name="app.celery_app.run_job_task")
def run_job_task(job_id: int):
    """
    Kuyruğa atılan her bir işin (job) çalıştırılmasını sağlayan ana Celery görevi.
    """
    # Veritabanı oturumunu açıyoruz
    db = SessionLocal()
    try:
        # 1. Job'u veritabanından çek
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return f"Error: Job ID {job_id} bulunamadı."
        
        # 2. İşin başladığını bildirmek için durumu "running" yap
        job.status = "running"
        db.commit()

        # 3. İlgili işin sınıfını factory sözlüğünden bul
        job_class = JOB_CLASSES.get(job.job_type)
        if not job_class:
            job.status = "failed"
            job.result = f"Desteklenmeyen job_type: {job.job_type}"
            db.commit()
            return job.result
        
        # 4. Sınıfı oluştur ve çalıştır
        job_instance = job_class()
        try:
            # Gerekli parametreyi (payload) vererek çalıştır
            result = job_instance.run(job.payload)
            
            # İşlem başarıyla biterse veritabanına kaydet
            job.status = "completed"
            job.result = result
            db.commit()
            return "Başarılı"
            
        except Exception as e:
            # Çalışma esnasında bir hata oluşursa yakala
            job.status = "failed"
            job.result = f"Görev çalıştırılırken hata: {str(e)}"
            db.commit()
            return job.result

    finally:
        # İşlem bitince veritabanı bağlantısını kapat
        db.close()
