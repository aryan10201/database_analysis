# Elyx Life – Member Journey API & Frontend

A comprehensive health journey tracking system that generates 8 months of WhatsApp-style communication between an Elyx member (Rohan Patel) and the Elyx team, builds a member journey timeline, and tracks internal metrics.

## 🎯 Features

### 1. Communication Message Generation 💬
- **8-month conversation simulation** with realistic health-related discussions
- **WhatsApp-style messaging** between Rohan Patel and Elyx team members
- **Various conversation types**: general queries, health plan updates, weekly reports, follow-ups
- **Realistic constraints**:
  - Full diagnostic test panel every 3 months
  - Member initiates ~5 conversations per week
  - 5 hours per week commitment (with 50% adherence)
  - Exercise updates every 2 weeks
  - Travel week every 4 weeks (Singapore-based member)

### 2. Journey Visualization 📈
- **Weekly timeline view** showing adherence, hours committed, and key events
- **Day-by-day inspection** with messages, events, and decisions
- **Decision tracking** explaining why specific interventions were made
- **Event correlation** linking messages to medical decisions

### 3. Internal Metrics Tracking 📊
- **Team effort monitoring**: doctor, coach, nutritionist, physio, and concierge hours
- **Intervention tracking**: total medical and lifestyle interventions
- **Performance analytics**: weekly and monthly summaries

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (tested with Python 3.13)
- Node.js 16+ and npm
- Windows PowerShell or Command Prompt

### Backend Setup (FastAPI)

1. **Navigate to backend directory:**
   ```bash
   cd elyx_fastapi_app
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the backend server:**
   ```bash
   # Option 1: Direct command
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
   
   # Option 2: Use the batch file (Windows)
   run_backend.bat
   ```

4. **Verify backend is running:**
   - Open http://localhost:8080 in your browser
   - You should see the API documentation

### Frontend Setup (Next.js)

1. **Navigate to frontend directory:**
   ```bash
   cd elyx_frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend development server:**
   ```bash
   # Option 1: Direct command
   npm run dev
   
   # Option 2: Use the batch file (Windows)
   run_frontend.bat
   ```

4. **Open the application:**
   - Navigate to http://localhost:3000
   - You should see the Elyx Dashboard

## 📱 Using the Application

### 1. Generate Data
- Start on the home page
- Click "Run Simulation" to generate 8 months of conversation data
- This creates the dataset needed for all other views

### 2. Explore Conversations
- **Chat View** (`/chat`): WhatsApp-style message interface
  - Filter by message type (member, team, weekly reports, questions, replies)
  - Search within messages
  - View message tags and relationships

### 3. View Journey Timeline
- **Timeline View** (`/timeline`): Weekly progress overview
  - See adherence percentages and hours committed
  - Click on weeks to inspect specific days
  - View events, decisions, and messages for each day

### 4. Monitor Metrics
- **Metrics View** (`/metrics`): Team performance dashboard
  - Track hours spent by each team member
  - Monitor intervention rates
  - View performance summaries

## 🔧 API Endpoints

### Conversations
- `POST /conversations/simulate` - Generate simulation data
- `GET /conversations` - List all conversations

### Journey
- `GET /journey/timeline` - Get complete timeline data
- `GET /journey/day?date=YYYY-MM-DD` - Get specific day details

### Metrics
- `GET /metrics` - Get team performance metrics

### Persona
- `GET /persona` - Get member profile information

## 🎨 Technical Details

### Backend Architecture
- **FastAPI** with automatic API documentation
- **Pydantic models** for data validation
- **Modular service structure** for maintainability
- **State persistence** using JSON files

### Frontend Features
- **Next.js 14** with React 18
- **Tailwind CSS** for responsive design
- **Real-time data fetching** from API
- **Interactive filtering and search**
- **Responsive design** for all screen sizes

### Data Generation Logic
- **Realistic conversation patterns** based on health goals
- **Travel scheduling** every 4 weeks
- **Diagnostic testing** every 3 months
- **Exercise progression** every 2 weeks
- **Adherence simulation** with 50% realistic compliance

## 🐛 Troubleshooting

### Common Issues

1. **Backend won't start:**
   - Ensure Python dependencies are installed: `pip install -r requirements.txt`
   - Check if port 8080 is available
   - Verify Python version (3.8+)

2. **Frontend won't start:**
   - Ensure Node.js dependencies are installed: `npm install`
   - Check if port 3000 is available
   - Verify Node.js version (16+)

3. **API calls failing:**
   - Ensure backend is running on http://localhost:8080
   - Check browser console for CORS errors
   - Verify API endpoints in browser at http://localhost:8080/docs

4. **No data showing:**
   - Run the simulation first from the home page
   - Check if the backend generated data successfully
   - Verify the data directory exists and contains state.json

### Getting Help
- Check the API documentation at http://localhost:8080/docs
- Review browser console for JavaScript errors
- Check terminal output for Python/Node.js errors

## 🎯 Next Steps

The system is designed to be extensible. Consider adding:
- **Real-time notifications** for new messages
- **Data export** functionality
- **Advanced analytics** and reporting
- **Integration** with real health data sources
- **Mobile app** version
- **Multi-member support**

## 📄 License

This project is part of the Elyx Life health journey tracking system.
