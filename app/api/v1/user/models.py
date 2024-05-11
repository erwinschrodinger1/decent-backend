from app.extensions import db, ma
from sqlalchemy import Column, Integer, DateTime, String, Text, func, ARRAY


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), nullable=False, unique=True)
    social_media = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    public_key_path = Column(Text, nullable=False)

    def __repr__(self):
        return f'<Event "{self.title}">'

    def __init__(self, username, public_key_path):
        self.username = username
        self.public_key_path = public_key_path
