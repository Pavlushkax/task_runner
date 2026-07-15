from abc import ABC, abstractmethod

class BaseJob(ABC):
    """
    Sisteme eklenecek tüm job'lar bu sınıftan türemek (miras almak) ZORUNDADIR.
    Bu sayede her job'ın mutlaka bir 'run' fonksiyonu olacağını garanti ederiz.
    """
    
    @abstractmethod
    def run(self, payload: str) -> str:
        """
        Her iş kendi çalışma mantığını bu fonksiyonun içine yazacak.
        Girdi olarak 'payload' alacak, sonuç olarak 'string' dönecek.
        """
        pass