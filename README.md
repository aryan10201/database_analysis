# Elyx Life – Member Journey API & Frontend

A comprehensive health journey tracking system that generates **8 months of WhatsApp-style communication** between an Elyx member and the Elyx team, builds a **member journey timeline**, and tracks **internal metrics**.

## ✨ Features

### AI-Powered Data Generation
- Integrated with **Groq AI** to generate realistic health journeys through API endpoints
- Simulated 8-month conversation history with WhatsApp-style messaging using Master Promts created after observing problem statement

### Journey Visualization
- Weekly timeline with adherence, commitment hours, and medical events
- Day-by-day view of conversations, events, and health decisions

### Decision & Metrics Tracking
- Tracks why interventions were made (diagnostics, lifestyle changes, etc.)
- Team effort monitoring across doctors, coaches, nutritionists, physios, and concierge
- Weekly and monthly performance analytics

## 🚀 Quick Start

### Backend Setup (FastAPI)

1. **Navigate to backend directory:**
```bash
cd elyx_fastapi_app
```

2. **Create and activate a virtual environment:**
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Start the backend server:**
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

5. **Verify backend is running:**
   - Open http://localhost:8080 in your browser
   - You should see the API documentation

### Frontend Setup (Next.js)

1. **Navigate to frontend directory:**
```bash
cd elyx_frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start the frontend development server:**
```bash
npm run dev
```

4. **Open the application:**
   - Navigate to http://localhost:3000
   - You should see the Elyx Dashboard

## 📡 API Endpoints

### Conversations
- `GET /conversations/{member_id}` – Get Conversations
- `GET /test-conversations/{member_id}` – Test Conversations

### Journey Generation
- `POST /generate-complete-journey` – Generate Complete Journey

### AI
- `GET /ai/models` – Get AI Models
- `GET /ai/health` – AI Health Check

### Journey
- `GET /journey/journey/timeline/{member_id}` – Get Journey Timeline
- `GET /journey/journey/conversations/{member_id}` – Get Conversations
- `GET /journey/journey/decisions/{member_id}` – Get Decisions
- `GET /journey/journey/metrics/{member_id}` – Get Metrics
- `GET /journey/journey/team-metrics/{member_id}` – Get Team Metrics
- `GET /journey/journey/decision-context/{decision_id}` – Get Decision Context

### Health
- `GET /health` – Health Check

## 🎨 Technical Details

- **Backend:** FastAPI with Pydantic models, modular service structure, and AI integration via Groq
- **Frontend:** Next.js 14, React 18, Tailwind CSS, responsive dashboard with interactive filtering/search
- **Data Logic:** Simulated conversation patterns, diagnostic testing every 3 months, exercise tracking, adherence simulation, and travel weeks every 4 weeks

## 🖥️ Using the Application

After running both **backend (FastAPI)** and **frontend (Next.js)**:

### 1. Dashboard Landing
- Visit http://localhost:3000
- You'll see the **Elyx Dashboard** with navigation to:
  - **Chat View** (WhatsApp-style conversation)
  - **Journey Timeline** (weekly health journey)
  - **Metrics Dashboard** (aggregated analytics)

### 2. Chat View
- Simulates **8 months of conversations** between a member and the Elyx team
- Shows:
  - Daily WhatsApp-style messages
  - Automated interventions (doctors, nutritionists, coaches, physios, concierge)
  - AI-generated personalization powered by **Groq**


### 3. Journey Timeline
- Weekly view of the member's journey
- Includes:
  - Adherence level (✅ full, ⚠ partial, ❌ missed)
  - Commitment hours (exercise, physio, nutrition, doctor sessions)
  - Diagnostics (blood tests, checkups, lab reports)
  - Lifestyle events (e.g., travel weeks, stress incidents)


### 4. Metrics Dashboard
- Aggregated **weekly & monthly metrics**
- Tracks:
  - **Commitment Hours** across doctor, coach, nutrition, physio, and concierge
  - **Adherence Trends** (weekly adherence levels)
  - **Decision Metrics** (why interventions were made – diagnostics, lifestyle, adherence, etc.)
  - **Team Metrics** (who contributed most to the member's journey)


### 5. AI Integration
- Elyx uses **Groq-powered AI models** for realistic data generation:
  - **Health conversation simulation**
  - **Decision-making context**
  - **Personalized intervention patterns**


### 6. Health Check
Verify backend health with:
```bash
GET /health
```

## 🔧 Project Structure

```
elyx-life/
├── elyx_fastapi_app/          # Backend FastAPI application
│   ├── app/
│   │   ├── main.py           # Main FastAPI application
│   │   └── ...
│   ├── requirements.txt      # Python dependencies
│   └── venv/                # Virtual environment
├── elyx_frontend/            # Frontend Next.js application
│   ├── components/          # React components
│   ├── pages/              # Next.js pages
│   ├── package.json        # Node.js dependencies
│   └── ...
└── README.md               # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🆘 Support

If you encounter any issues or have questions:

1. Check the API documentation at http://localhost:8080 when the backend is running
2. Ensure both backend and frontend are running on their respective ports
3. Verify all dependencies are installed correctly

---

**Built with ❤️ by the Team Synergy**