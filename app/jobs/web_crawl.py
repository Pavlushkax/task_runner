import subprocess
from app.jobs.base import BaseJob

class WebCrawlJob(BaseJob):
    def run(self, payload: str) -> str:
        try:
            # Katana komutunu hazırlıyoruz. 
            # '-silent' parametresi sadece bulunan URL'leri basmasını sağlar, gereksiz logları temizler.
            cmd = f"katana -u {payload} -silent"
            
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=300 # Web taraması uzun sürebileceği için 5 dakika süre verdik
            )
            
            if result.returncode != 0:
                return f"Katana Hatası:\n{result.stderr}"
            
            # Çıkan logları satır satır bölüyoruz
            urls = result.stdout.strip().split("\n")
            
            # Eğer çıktı tamamen boşsa 0, doluysa satır sayısını alıyoruz
            total_urls = len(urls) if result.stdout.strip() else 0
            
            return f"Tarama tamamlandı. Toplam {total_urls} adet benzersiz URL adresi bulundu ve kaydedildi."
            
        except Exception as e:
            return f"Katana Çalıştırılırken Hata Oluştu: {str(e)}"