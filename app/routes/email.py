from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db  ## DB session dependency
from app.services.ms_graph import fetch_email_by_id
from app.services.email_parser import save_email_to_db
import httpx
router = APIRouter()

GRAPH_URL = "https://graph.microsoft.com/v1.0/me/messages"

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
        saved_email = save_email_to_db(email_data, db)
        return {"status": "success", "email_id": str(saved_email.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save email: {str(e)}")


@router.get("/emails/fetch")
async def fetch_emails(Authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    Fetch emails using Microsoft Graph API and save to the database
    """
    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    access_token = Authorization.split(" ")[1]

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(GRAPH_URL, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch emails", "details": response.json()}

    data = response.json()

    saved = []
    for msg in data.get("value", []):
        email = Email(
            subject=msg.get("subject"),
            sender_mail_id=msg.get("from", {}).get("emailAddress", {}).get("address"),
            revicer_mail_id=msg.get("toRecipients", [{}])[0].get("emailAddress", {}).get("address"),
            content_encoding="utf-8",
            content=msg.get("body", {}).get("content", ""),
            datetime_format=datetime.strptime(msg.get("receivedDateTime"), "%Y-%m-%dT%H:%M:%SZ"),
            has_attachment=msg.get("hasAttachments", False),
            org_id="your_org_id",   # Fill in from token or session
            admin_mail_id="admin@example.com",  # Fill in properly
        )
        db.add(email)
        saved.append(email)

    db.commit()
    return {"message": f"Saved {len(saved)} emails"}
