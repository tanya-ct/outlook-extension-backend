from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import re
import uuid
from datetime import datetime

"""""" """""" """ SAVE ATTACHMENT SCHEMA """ """""" """""" 

class AttachmentSchema(BaseModel):
    id: Optional[uuid.UUID]
    name: Optional[str]
    doc_link: Optional[str]

    class Config:
        orm_mode = True

"""""" """""" """ SAVE THREAD SCHEMA """ """""" """""" 

class EmailThreadSchema(BaseModel):
    id: Optional[uuid.UUID]
    thread_index: Optional[str]
    references: Optional[str]
    in_reply_to: Optional[str]
    subject: Optional[str]
    sender_mail_id: Optional[str]
    revicer_mail_id: Optional[str]
    cc_reciver_mail_id: Optional[str]
    bcc_reciver_mail_id: Optional[str]
    content_encoding: Optional[str]
    content: Optional[str]
    datetime_format: Optional[datetime]
    has_attachment: bool = False
    attachments: List[AttachmentSchema] = []

    class Config:
        orm_mode = True

"""""" """""" """ SAVE EMAIL SCHEMA """ """""" """""" 

class EmailSchema(BaseModel):
    id: Optional[uuid.UUID]
    ms_graph_id = str
    org_id: Optional[str]
    admin_mail_id: Optional[str]
    subject: Optional[str]
    sender_mail_id: Optional[str]
    revicer_mail_id: Optional[str]
    cc_reciver_mail_id: Optional[str]
    bcc_reciver_mail_id: Optional[str]
    content_encoding: Optional[str]
    content: Optional[str]
    datetime_format: Optional[datetime]
    has_attachment: bool = False
    has_thread: bool = False
    attachments: List[AttachmentSchema] = []
    threads: List[EmailThreadSchema] = []

    class Config:
        orm_mode = True
