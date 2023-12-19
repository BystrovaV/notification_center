from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    def send_email(self, email: str, text: str):
        pass
