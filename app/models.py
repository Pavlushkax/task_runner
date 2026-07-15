from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base

# 1. Veritabanındaki tablomuzu temsil edecek olan Python sınıfını (Model) tanımlıyoruz.
# Bu sınıf, database.py içinde oluşturduğumuz "Base" sınıfından türemek zorunda.
class Job(Base):
    # Veritabanında bu tablonun adı "jobs" olacak.
    __tablename__ = "jobs"

    # 2. Kolonlarımızı ve veri tiplerini belirliyoruz.
    
    # Her işin (job) benzersiz bir numarası olacak. Otomatik artan bir sayı.
    id = Column(Integer, primary_key=True, index=True)
    
    # İşin türü. "os_command" mi yoksa "katana" mı olduğunu burada tutacağız.
    job_type = Column(String, nullable=False)
    
    # İşin o anki durumu. Varsayılan olarak (default) "pending" yani "bekliyor" başlayacak.
    # Süreç ilerledikçe bu durum "running", "completed" veya "failed" olarak güncellenecek.
    status = Column(String, default="pending", nullable=False)
    
    # İşe gönderilen girdi (parametre). Örn: "ls -la" veya "https://example.com"
    payload = Column(String, nullable=False)
    
    # İş bittiğinde arka plandaki worker'ın ürettiği sonuç buraya yazılacak.
    # Başlangıçta boş olabileceği için nullable=True (boş bırakılabilir) yapıyoruz.
    result = Column(Text, nullable=True)
    
    # İşin sisteme eklendiği tarih ve saat. default=datetime.utcnow sayesinde otomatik kaydedilir.
    created_at = Column(DateTime, default=datetime.utcnow)