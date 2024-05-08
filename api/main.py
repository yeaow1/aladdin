from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
from dotenv import load_dotenv
from database import postgres
import os

load_dotenv()

app = FastAPI(title="Aladdin Bot, Full API", description="Docs for Aladdin Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/oauth/callback")
async def oauth_callback(request: Request):

    code = request.query_params
    if not code.get("code"):
        raise HTTPException(detail="Invalid request, code not found", status_code=404)

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://discord.com/api/oauth2/token",
            data={
                "client_id": os.environ["CLIENT_ID"],
                "client_secret": os.environ["CLIENT_SECRET"],
                "grant_type": "authorization_code",
                "code": code.get("code"),
                "redirect_uri": os.environ["REDIRECT_URI"],
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        ) as response:
            data = await response.json()
            return JSONResponse(content=data, status_code=200)


@app.get("/users/@me")
async def get_current_user(request: Request, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            "https://discord.com/api/users/@me", headers=headers
        )
        data = await response.json()

        if response.status != 200:
            return JSONResponse(
                content={"error": "Failed to fetch user data", "details": data},
                status_code=response.status,
            )

        return JSONResponse(content=data, status_code=200)


@app.get("/users/@me/guilds")
async def get_guilds_user(request: Request, token: str):
    headers = {"Authorization": f"Bearer {token}"}

    async with aiohttp.ClientSession() as session:
        response = await session.get(
            "https://discord.com/api/users/@me/guilds", headers=headers
        )
        data = await response.json()

        if response.status != 200:
            return JSONResponse(
                content={"error": "Failed to fetch user guilds", "details": data},
                status_code=response.status,
            )

        return JSONResponse(content=data, status_code=200)
