import httpx
from datetime import datetime
from app.models.email import Email

GRAPH_URL = "https://graph.microsoft.com/v1.0/me/messages?$select=id,subject,from,toRecipients,receivedDateTime,hasAttachments"


async def fetch_email_by_id(email_id: str, access_token: str):
    url = f"https://graph.microsoft.com/v1.0/me/messages/{email_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")
        return response.json()


async def fetch_all_emails(access_token: str, db):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(GRAPH_URL, headers=headers)
        response.raise_for_status()
        data = response.json()

        saved = 0
        for msg in data.get("value", []):
            email_id = msg.get("id")
            if db.query(Email).filter_by(ms_graph_id=email_id).first():
                continue

            detail_url = f"https://graph.microsoft.com/v1.0/me/messages/{email_id}"
            detail_resp = await client.get(detail_url, headers=headers)
            detail_resp.raise_for_status()
            msg_data = detail_resp.json()

            email = Email(
                ms_graph_id=email_id,
                subject=msg_data.get("subject"),
                sender_mail_id=msg_data.get("from", {}).get("emailAddress", {}).get("address"),
                revicer_mail_id=msg_data.get("toRecipients", [{}])[0].get("emailAddress", {}).get("address"),
                content_encoding="utf-8",
                content=msg_data.get("body", {}).get("content", ""),
                datetime_format=datetime.strptime(msg_data.get("receivedDateTime"), "%Y-%m-%dT%H:%M:%SZ"),
                has_attachment=msg_data.get("hasAttachments", False),
                org_id="test_org_id",
                admin_mail_id="admin-test@example.com",
            )
            db.add(email)
            saved += 1

        db.commit()
        return saved
