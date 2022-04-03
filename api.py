import asyncio

import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
import google.oauth2
from google.oauth2 import *
import google.auth

st.title("Google OAuth2 flow")

"## Configuration"

client_id = st.text_input("Client ID")
client_secret = st.text_input("Client secret")
redirect_uri = st.text_input("Redirect URI", "http://localhost:8000/redirect")

if client_id and client_secret and redirect_uri:
    client = GoogleOAuth2(client_id, client_secret)
else:
    client = None

"## Authorization URL"


async def write_authorization_url():
    authorization_url = await client.get_authorization_url(
        redirect_uri,
        scope=["profile", "email"],
        extras_params={"access_type": "offline"},
    )
    st.write(authorization_url)


if client:
    asyncio.run(write_authorization_url())
else:
    "Waiting client configuration..."

"## Callback"

if client:
    code = st.text_input("Authorization code")
else:
    code = None
    "Waiting client configuration..."

"## Access token"


async def write_access_token(code):
    token = await client.get_access_token(code, redirect_uri)
    st.write(token)


if code:
    asyncio.run(write_access_token(code))
else:
    "Waiting authorization code..."