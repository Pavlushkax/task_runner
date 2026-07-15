# Task Runner API

Bu proje, asenkron arka plan görevlerini yönetmek için tasarlanmış, Docker üzerinde çalışan bir RESTful API servisidir. Sistem, kullanıcıdan aldığı görevleri (job) sıraya sokar, arka planda işletir ve sonuçlarını bir veritabanına kaydeder.

## 🚀 Teknolojiler
- **FastAPI**: Hızlı ve modern RESTful API sunucusu.
- **Celery**: Asenkron görev yöneticisi (Background Worker).
- **Redis**: Mesaj kuyruğu (Message Broker).
- **SQLite & SQLAlchemy**: Veritabanı ve ORM yapısı.
- **Docker & Docker Compose**: Tam izole konteyner mimarisi.
- **Katana (ProjectDiscovery)**: Harici web tarama aracı entegrasyonu.

## 🛠 Mimari Özellikleri
- **Asenkron İşleyiş**: API, gelen istekleri anında kabul edip kullanıcıyı bekletmeden işi arka plana (Celery) atar.
- **Factory Pattern**: Yeni bir iş (job) modeli eklemek son derece esnektir. Çekirdek kodu bozmadan sadece yeni bir sınıf yazılarak sisteme entegre edilebilir.
- **Konteynerizasyon**: Tüm servisler `docker-compose` ile birbirine bağlı ancak izole bir şekilde çalışır. Bilgisayara ek bir veritabanı veya kütüphane kurmaya gerek yoktur.

## 💻 Nasıl Çalıştırılır?
Sistemi ayağa kaldırmak için bilgisayarınızda **Docker** yüklü olması yeterlidir.

1. Projeyi klonlayın ve dizine gidin:
```bash
git clone https://github.com/Pavlushkax/task_runner.git
cd task_runner
```

2. Konteynerleri inşa edin ve başlatın:
```bash
docker-compose up --build
```

3. Tarayıcınızda Swagger arayüzüne gidin ve API'yi test edin:
👉 **`http://localhost:8000/docs`**

## 📌 Kullanım (Endpoints)
- **POST `/jobs`**: Sisteme yeni bir görev ekler.
  - Örnek `os_command` payload'u: `{"job_type": "os_command", "payload": "ls -la"}`
  - Örnek `katana` payload'u: `{"job_type": "katana", "payload": "https://books.toscrape.com/"}`
- **GET `/jobs/{id}`**: Gönderilen görevin o anki durumunu (`pending`, `running`, `completed`) ve bittiyse sonucunu (`result`) getirir.
- **GET `/jobs`**: Sistemdeki tüm görev geçmişini listeler.
