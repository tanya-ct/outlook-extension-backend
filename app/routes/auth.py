from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import RedirectResponse, JSONResponse
from urllib.parse import urlencode
import httpx
from app.config import settings

router = APIRouter()

AUTHORITY = f"https://login.microsoftonline.com/{settings.azure_tenant_id}"
AUTH_URL = f"{AUTHORITY}/oauth2/v2.0/authorize"
TOKEN_URL = f"{AUTHORITY}/oauth2/v2.0/token"
SCOPE = "User.Read Mail.Read"  

@router.get("/auth/login")
async def login():
    params = {
        "client_id": settings.azure_client_id,
        "response_type": "code",
        "redirect_uri": settings.azure_redirect_uri,
        "response_mode": "query",
        "scope": SCOPE,
        "state": "12345"  # Optional state to validate callback
    }
    url = f"{AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(url)

@router.get("/getToken")
async def auth_callback(request: Request):
    code = request.query_params.get("code")

    if not code:
        return JSONResponse({"error": "No code provided"}, status_code=400)

    data = {
        "client_id": settings.azure_client_id,
        "client_secret": settings.azure_client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.azure_redirect_uri,
        "scope": SCOPE,
    }
    async with httpx.AsyncClient() as client:
        token_response = await client.post(TOKEN_URL, data=data, 
            headers={"Content-Type": "application/x-www-form-urlencoded"})
    print("Status Code:", token_response.status_code)
    print("Text Response:", token_response.text)
    if token_response.status_code != 200:
        return JSONResponse({"error": "Token exchange failed", "details": token_response.json()}, status_code=token_response.status_code)

    tokens = token_response.json()
    return tokens  # includes access_token, refresh_token, etc.
