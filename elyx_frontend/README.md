# Elyx Frontend (Next.js + Tailwind)

A minimal frontend for the Elyx Life Hackathon API.

## Setup

```bash
npm install
npm run dev
```

By default, it expects the FastAPI backend at `http://localhost:8080`.  
Override with an env var:

```bash
# in .env.local
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8080
```

## Pages

- `/` – dashboard: trigger simulation, quick links, persona
- `/chat` – WhatsApp-style message view
- `/timeline` – weekly timeline + day inspector
- `/metrics` – internal metrics
