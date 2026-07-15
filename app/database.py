from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Veritabanının bilgisayarda nereye kaydedileceğini seçiyoruz.
# Şimdilik proje klasöründe "sql_app.db" adında bir SQLite dosyası oluşacak.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 2. Veritabanı motorunu (engine) oluşturuyoruz.
# SQLite kullandığımız için "check_same_thread=False" ayarını ekliyoruz.
# Bu ayar, FastAPI'nin veritabanına hızlı ve güvenli bağlanmasını sağlar.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Veritabanında işlem (ekleme, silme, güncelleme) yapabilmek için 
# bir oturum (session) fabrikası kuruyoruz.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Bu "Base" sınıfı bizim için sihirli bir köprü.
# Birazdan models.py içinde yazacağımız tablolar bu sınıftan türeyecek.
Base = declarative_base()