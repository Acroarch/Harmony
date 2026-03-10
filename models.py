from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Column, String, Boolean, Text, DateTime,
    ForeignKey, Enum, Integer
)
from sqlalchemy.orm import relationship

from database import Base
from info_classes import MessageType, ServerInfo, UserInfo, MessageInfo  # noqa: F401


# FriendStatus is new — not in info_classes.py
class FriendStatus(PyEnum):
    Pending = "Pending"
    Accepted = "Accepted"
    Blocked = "Blocked"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    profile_image = Column(String(255), nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    owned_servers = relationship("Server", back_populates="owner")
    server_memberships = relationship("ServerMember", back_populates="user")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    friendships_initiated = relationship("Friend", foreign_keys="Friend.user_id_1", back_populates="user1")
    friendships_received = relationship("Friend", foreign_keys="Friend.user_id_2", back_populates="user2")


class Server(Base):
    __tablename__ = "servers"

    server_id = Column(Integer, primary_key=True, autoincrement=True)
    server_name = Column(String(100), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="owned_servers")
    members = relationship("ServerMember", back_populates="server")
    messages = relationship("Message", back_populates="server")


class ServerMember(Base):
    __tablename__ = "server_members"

    server_id = Column(Integer, ForeignKey("servers.server_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    joined_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    server = relationship("Server", back_populates="members")
    user = relationship("User", back_populates="server_memberships")


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    sender_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)  # Used for DMs
    server_id = Column(Integer, ForeignKey("servers.server_id"), nullable=True)  # Used for server messages
    message_type = Column(Enum(MessageType), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    server = relationship("Server", back_populates="messages")


class Friend(Base):
    __tablename__ = "friends"

    user_id_1 = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    user_id_2 = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    status = Column(Enum(FriendStatus), default=FriendStatus.Pending, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user1 = relationship("User", foreign_keys=[user_id_1], back_populates="friendships_initiated")
    user2 = relationship("User", foreign_keys=[user_id_2], back_populates="friendships_received")
