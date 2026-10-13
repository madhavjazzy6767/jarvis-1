# J.A.R.V.I.S. setup (iPad, no computer)
Structure: index.html (whole frontend) · server.py (optional FastAPI proxy) · .env.example

## Fastest: private test, no backend
1. On github.com (Safari) create a repo, upload index.html, Settings → Pages → deploy from main. You get an https:// URL (required for camera/mic).
2. Open it in Safari → ☰ → Settings → paste your Anthropic API key → Save. Key stays in memory unless you tick "Save key". Never publish a page with a key inside it.
## Secure: with backend + live search
Deploy the folder to Render/Railway/Fly (start: `uvicorn server:app --host 0.0.0.0 --port $PORT`, install: `pip install fastapi uvicorn httpx`). Set env vars from .env.example (Tavily offers a free search key). Open the app URL; keys never reach the browser. If the frontend is hosted elsewhere, put the backend URL in Settings.
## Permissions
Camera: tap Enable camera → Allow. Mic: tap 🎙 → Allow. If denied: Safari aA → Website Settings.
## Troubleshooting
Camera: needs https; check Website Settings; close other camera apps. Mic: Siri & Dictation must be on; Safari on iOS 14.5+ supports recognition, else use typed chat/keyboard dictation. API errors: Settings → Diagnostics; 401 key, 404 model name, 429 wait. 3D: Settings → Diagnostics shows WebGL; disable Low Power Mode.
## Checklist
Working in-browser: chat, context, voice in/out (browser-dependent), hand tracking, 3D globe + touch/wheel/gesture control, markers, timer/open/focus commands, history, diagnostics.
Needs external: AI key; live search (backend + Tavily key); HTTPS hosting; camera/mic permissions.
Not possible: controlling iPad system functions; a timer survives only while the page is open.
