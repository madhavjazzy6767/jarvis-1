"""Optional JARVIS backend: keeps API keys server-side, proxies AI + search, serves index.html.
Run: pip install fastapi uvicorn httpx && uvicorn server:app --host 0.0.0.0 --port 8000"""
import os, httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","), allow_methods=["*"], allow_headers=["*"])
@app.get("/api/health")
def health(): return {"ok": True, "ai": bool(os.getenv("ANTHROPIC_API_KEY")), "search": bool(os.getenv("TAVILY_API_KEY"))}
@app.post("/api/chat")
async def chat(req: Request):
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key: return JSONResponse({"error": "ANTHROPIC_API_KEY not set"}, 500)
    async with httpx.AsyncClient(timeout=60) as c:
        r = await c.post("https://api.anthropic.com/v1/messages", json=await req.json(),
            headers={"x-api-key": key, "anthropic-version": "2023-06-01"})
    return JSONResponse(r.json(), r.status_code)
@app.post("/api/search")
async def search(req: Request):
    key = os.getenv("TAVILY_API_KEY")
    if not key: return JSONResponse({"error": "TAVILY_API_KEY not set"}, 503)
    q = (await req.json()).get("q", "")
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.post("https://api.tavily.com/search", json={"api_key": key, "query": q, "max_results": 5})
    if r.status_code != 200: return JSONResponse({"error": "search failed"}, 502)
    return {"results": [{"title": x["title"], "url": x["url"], "content": x["content"][:500]} for x in r.json().get("results", [])]}
@app.get("/")
def index(): return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))
