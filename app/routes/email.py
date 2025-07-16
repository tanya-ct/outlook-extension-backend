from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db  ## DB session dependency
from app.services.ms_graph import fetch_email_by_id
from app.services.email_parser import save_email_to_db
import httpx
from datetime import datetime
from app.models.email import Email


router = APIRouter()

GRAPH_URL = "https://graph.microsoft.com/v1.0/me/messages?$select=id,subject,from,toRecipients,receivedDateTime,hasAttachments"


@router.post("/save-email/{email_id}")
async def save_email(
    email_id: str,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    access_token = authorization.replace("Bearer ", "")
    
    try:
        email_data = await fetch_email_by_id(email_id, access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch email: {str(e)}")
    
    try:
        existing = db.query(Email).filter_by(ms_graph_id=email_id).first()
        if existing:
            return {"status": "Duplicate, Email already Saved", "email_id": str(email_id)}
        else:
            saved_email = save_email_to_db(email_data, db)
            return {"status": "success", "email_id": str(saved_email.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save email: {str(e)}")



@router.get("/emails/fetch")
async def fetch_emails(Authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    Fetch emails using Microsoft Graph API and save to the database
    """
    if not Authorization.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="Invalid token format")

    access_token = Authorization.split(" ")[1]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(GRAPH_URL, headers=headers) 

        print("Status:", response.status_code)
        print("Text:", response.text)

        try:
            data = response.json()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Failed to decode JSON response from Microsoft Graph",
                    "error": str(e),
                    "raw_response": response.text
                }
            )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=data)

        saved = []
        for msg in data.get("value", []):
            try:
                email_id = msg["id"] ## create new feild to save this also 
                existing = db.query(Email).filter_by(ms_graph_id=email_id).first()
                if existing:
                    continue

                message_url = f"https://graph.microsoft.com/v1.0/me/messages/{email_id}"
                msg_detail = await client.get(message_url, headers=headers)
                msg_data = msg_detail.json()

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
                print(email.content)
                db.add(email)
                saved.append(email)

            except Exception as e:
                print(f"Failed to parse/save email: {e}")

    db.commit()
    return {"message": f"Saved {len(saved)} emails"}
