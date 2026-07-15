FROM python:3.10-slim

# Katana aracı ve diğer sistem gereksinimleri için gerekli paketleri yüklüyoruz
RUN apt-get update && apt-get install -y wget unzip && rm -rf /var/lib/apt/lists/*

# ProjectDiscovery'nin Katana aracını indirip kuruyoruz
RUN wget https://github.com/projectdiscovery/katana/releases/download/v1.0.5/katana_1.0.5_linux_amd64.zip && \
    unzip katana_1.0.5_linux_amd64.zip -d /usr/local/bin/ && \
    rm katana_1.0.5_linux_amd64.zip

# Çalışma dizinini ayarlıyoruz
WORKDIR /app

# Bağımlılıkları kopyalayıp kuruyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyalıyoruz
COPY . .

# Python'un çıktıları anında ekrana basması için ortam değişkeni
ENV PYTHONUNBUFFERED=1

# Varsayılan komut olarak FastAPI uygulamasını çalıştırıyoruz
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
