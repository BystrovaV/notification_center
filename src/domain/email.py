import dataclasses
from dataclasses import dataclass


@dataclass
class Email:
    to_address: str
    subject: str
    message: str

    id: str | None = None

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)
