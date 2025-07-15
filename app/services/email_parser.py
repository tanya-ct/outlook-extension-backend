from app.models.email import Email, Attachment
from sqlalchemy.orm import Session
from datetime import datetime

def save_email_to_db(email_data: dict, db: Session) -> Email:
    sender = email_data.get("from", {}).get("emailAddress", {}).get("address")
    to_recipients = ", ".join([r["emailAddress"]["address"] for r in email_data.get("toRecipients", [])])
    cc_recipients = ", ".join([r["emailAddress"]["address"] for r in email_data.get("ccRecipients", [])])
    bcc_recipients = ", ".join([r["emailAddress"]["address"] for r in email_data.get("bccRecipients", [])])

    email = Email(
        org_id="default-org",  # Replace if needed
        admin_mail_id="admin@example.com",  # Replace if needed
        subject=email_data.get("subject"),
        sender_mail_id=sender,
        revicer_mail_id=to_recipients,
        cc_reciver_mail_id=cc_recipients,
        bcc_reciver_mail_id=bcc_recipients,
        content_encoding=email_data.get("body", {}).get("contentType"),
        content=email_data.get("body", {}).get("content"),
        datetime_format=datetime.strptime(email_data["sentDateTime"], "%Y-%m-%dT%H:%M:%SZ"),
        has_attachment=email_data.get("hasAttachments", False),
        has_thread=False  # Optional: set to True if you're handling threads
    )

    db.add(email)
    db.flush()  # So that email.id is available

    # Optional: handle attachments
    for att in email_data.get("attachments", []):
        attachment = Attachment(
            email_id=email.id,
            name=att.get("name"),
            doc_link=att.get("@odata.mediaContentType", "")  # placeholder, update if you're storing links
        )
        db.add(attachment)

    db.commit()
    db.refresh(email)
    return email
