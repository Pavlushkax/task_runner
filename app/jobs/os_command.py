import subprocess
from app.jobs.base import BaseJob

class OSCommandJob(BaseJob):
    def run(self, payload: str) -> str:
        try:
            # shell=True sayesinde terminal komutlarını doğrudan çalıştırabiliriz.
            # capture_output=True ise komutun ekran çıktısını yakalamamızı sağlar.
            result = subprocess.run(
                payload, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=30  # Komut sonsuza kadar kilitli kalmasın diye 30 saniye sınır koyduk
            )
            
            # Eğer komut hata kodu döndüyse (stderr doluysa) hatayı dön
            if result.returncode != 0:
                return f"Hata Oluştu:\n{result.stderr}"
                
            # Komut başarıyla çalıştıysa ekran çıktısını dön
            return result.stdout
            
        except Exception as e:
            return f"Sistem Hatası: {str(e)}"