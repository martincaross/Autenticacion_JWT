from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    __tablename__: "User"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    fullname: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "fullname": self.fullname
            # do not serialize the password, its a security breach
        }
    
class Address(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    street_name: Mapped[str] = mapped_column(String(120), unique=False, nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False)



    def serialize(self):
        return {
            "id": self.id,
            "street_name": self.street_name,
            "city": self.city
            # do not serialize the password, its a security breach
        }