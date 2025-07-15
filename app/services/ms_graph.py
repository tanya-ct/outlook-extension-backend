import httpx

GRAPH_API = "https://graph.microsoft.com/v1.0"

async def fetch_email_by_id(email_id: str, access_token: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        res = await client.get(f"{GRAPH_API}/me/messages/{email_id}", headers=headers)
        if res.status_code != 200:
            raise Exception(f"Graph error: {res.status_code}, {res.text}")
        return res.json()
