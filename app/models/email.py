from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

"""""" """""" """ SAVE EMAIL MODEL """ """""" """""" 

class Email(Base):
    __tablename__ = "emails"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ms_graph_id = Column(String, unique=True, index=True)
    org_id = Column(String)
    admin_mail_id = Column(String)
    subject = Column(String)
    sender_mail_id = Column(String)
    revicer_mail_id = Column(String)
    cc_reciver_mail_id = Column(String)
    bcc_reciver_mail_id = Column(String)
    content_encoding = Column(String)
    content = Column(Text)
    datetime_format = Column(DateTime)
    has_attachment = Column(Boolean, default=False)
    has_thread = Column(Boolean, default=False)

    attachments = relationship("Attachment", back_populates="email", cascade="all, delete-orphan")
    threads = relationship("EmailThread", back_populates="email", cascade="all, delete-orphan")

"""""" """""" """ SAVE ATTACHMENT MODEL """ """""" """""" 

class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id = Column(UUID(as_uuid=True), ForeignKey("emails.id"))
    thread_id = Column(UUID(as_uuid=True), ForeignKey("threads.id"), nullable=True)
    name = Column(String)
    doc_link = Column(String)

    email = relationship("Email", back_populates="attachments")
    thread = relationship("EmailThread", back_populates="attachments")

"""""" """""" """ EMAIL THREAD MODEL """ """""" """""" 

class EmailThread(Base):
    __tablename__ = "threads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id = Column(UUID(as_uuid=True), ForeignKey("emails.id"))  # Parent Email
    thread_index = Column(String)
    references = Column(String)
    in_reply_to = Column(String)
    subject = Column(String)
    sender_mail_id = Column(String)
    revicer_mail_id = Column(String)
    cc_reciver_mail_id = Column(String)
    bcc_reciver_mail_id = Column(String)
    content_encoding = Column(String)
    content = Column(Text)
    datetime_format = Column(DateTime)
    has_attachment = Column(Boolean, default=False)

    email = relationship("Email", back_populates="threads")
    attachments = relationship("Attachment", back_populates="thread", cascade="all, delete-orphan")



