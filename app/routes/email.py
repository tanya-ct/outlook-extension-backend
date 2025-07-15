from fastapi import APIRouter, Header, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db  ## DB session dependency
from app.services.ms_graph import fetch_email_by_id
from app.services.email_parser import save_email_to_db

router = APIRouter()

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
