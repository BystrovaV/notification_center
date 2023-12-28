from pydantic import BaseModel, EmailStr

from domain.email import Email


class EmailInput(BaseModel):
    to_address: EmailStr
    subject: str
    message: str

    def to_entity(self):
        return Email(
            to_address=self.to_address, subject=self.subject, message=self.message
        )
