from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Election(Base):
    __tablename__ = "elections"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    is_active = Column(Boolean, default=True)

    votes = relationship("EncryptedVote", back_populates="election")


class Voter(Base):
    __tablename__ = "voters"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    has_voted = Column(Boolean, default=False)
    election_id = Column(Integer, ForeignKey("elections.id"))


class EncryptedVote(Base):
    __tablename__ = "encrypted_votes"

    id = Column(Integer, primary_key=True, index=True)
    encrypted_payload = Column(Text, nullable=False)  # voto cifrado
    timestamp = Column(DateTime, default=datetime.utcnow)
    election_id = Column(Integer, ForeignKey("elections.id"))

    election = relationship("Election", back_populates="votes")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

