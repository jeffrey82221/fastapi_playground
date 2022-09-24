"""
Porting the local api to the internet
"""
import nest_asyncio
from pyngrok import ngrok
import uvicorn
from executor_api import app
ngrok.set_auth_token("296zATB6WYNOnhCSqlQJYyxwTor_69pPVvPvKTrskkTva7ok")
ngrok_tunnel = ngrok.connect(9999)
print('Public URL:', ngrok_tunnel.public_url)
nest_asyncio.apply()
uvicorn.run(app, port=9999)
