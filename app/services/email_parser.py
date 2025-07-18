from app.models.email import Email


def save_email_if_not_exists(email_data: dict, db):
    ms_graph_id = email_data.get("id")
    if db.query(Email).filter_by(ms_graph_id=ms_graph_id).first():
        return {"status": "Duplicate, Email already Saved", "email_id": ms_graph_id}

    email = Email(
        ms_graph_id=ms_graph_id,
        subject=email_data.get("subject"),
        sender_mail_id=email_data.get("from", {}).get("emailAddress", {}).get("address"),
        revicer_mail_id=email_data.get("toRecipients", [{}])[0].get("emailAddress", {}).get("address"),
        content_encoding="utf-8",
        content=email_data.get("body", {}).get("content", ""),
        datetime_format=email_data.get("receivedDateTime"),
        has_attachment=email_data.get("hasAttachments", False),
        org_id="test_org_id",
        admin_mail_id="admin-test@example.com",
    )

    db.add(email)
    db.commit()
    db.refresh(email)
    return {"status": "success", "email_id": str(email.id)}
