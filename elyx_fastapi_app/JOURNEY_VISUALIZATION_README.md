# Elyx Life - Journey Visualization System

## Overview

This system provides a comprehensive visualization of a member's 8-month health optimization journey, including:

- **Conversation Generation**: AI-generated WhatsApp-style conversations using local LLM (Ollama)
- **Decision Tracking**: Complete traceability from conversations to health decisions
- **Timeline Visualization**: Month-by-month breakdown of the journey
- **Team Metrics**: Tracking of hours spent by different team members
- **Database Storage**: All data is persisted for analysis and visualization

## Key Features

### 1. Local AI Integration
- Uses Ollama for conversation generation (100% free, no API costs)
- Generates realistic health coaching conversations
- Creates episode-specific content for each month

### 2. Decision Tracking
- Every health decision is linked to specific conversations
- Click on any decision to see the exact context that led to it
- Complete audit trail for compliance and analysis

### 3. Comprehensive Visualization
- **Journey Timeline**: Month-by-month view with health events and decisions
- **Team Metrics Dashboard**: Charts showing team member hours and interventions
- **Interactive Elements**: Click to explore decision context and supporting conversations

## System Architecture

### Backend (FastAPI)
```
app/
├── models/
│   ├── database.py      # Database models with enhanced tracking
│   └── schemas.py       # Pydantic schemas for API responses
├── services/
│   ├── local_ai_service.py    # Ollama integration for AI generation
│   └── journey_service.py     # Journey generation and storage logic
├── routes/
│   └── journey.py             # API endpoints for journey data
└── main.py                    # FastAPI application with new routes
```

### Frontend (Next.js)
```
elyx_frontend/
├── components/
│   ├── JourneyTimeline.js           # Timeline visualization component
│   └── TeamMetricsDashboard.js      # Team metrics dashboard
├── pages/
│   └── journey.js                   # Main journey page
└── package.json                     # Dependencies including date-fns and recharts
```

## Database Schema

### Enhanced Models
- **Conversation**: Stores all messages with month/week tracking and decision impact
- **Decision**: Health decisions with links to triggering and supporting conversations
- **HealthEvent**: Medical events, tests, and plan modifications
- **MemberMetrics**: Weekly adherence and progress tracking
- **TeamMetrics**: Hours spent by different team roles

### Key Relationships
- Conversations → Decisions (via `decision_impact`)
- Decisions → Conversations (via `supporting_conversations`)
- Events → Conversations and Decisions (via `linked_conversations`)

## Installation & Setup

### 1. Backend Setup
```bash
cd elyx_fastapi_app

# Install dependencies
pip install -r requirements.txt

# Install Ollama (for local AI)
# Follow instructions at: https://ollama.ai/

# Pull required model
ollama pull llama2

# Initialize database
python init_database.py

# Start backend
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd elyx_frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

## Usage

### 1. Generate Journey
- Navigate to `/journey` page
- Click "Generate New Journey" button
- System will create 8 months of conversations, decisions, and events
- All data is stored in the database

### 2. View Timeline
- **Journey Timeline Tab**: Month-by-month breakdown
- Click on month buttons to filter view
- Click on decisions to see conversation context
- View health events and progress metrics

### 3. Analyze Team Performance
- **Team Metrics Tab**: Comprehensive dashboard
- Bar charts showing monthly hours by role
- Pie chart showing total hours distribution
- Detailed table with all metrics

### 4. Decision Context
- Click "View Decision Context" on any decision
- See the exact conversation that triggered the decision
- View all supporting conversations
- Understand the reasoning behind each health decision

## API Endpoints

### Journey Generation
- `POST /generate-complete-journey` - Generate and store complete journey
- `POST /journey/generate/{member_id}` - Generate journey for specific member

### Data Retrieval
- `GET /journey/timeline/{member_id}` - Get complete timeline data
- `GET /journey/conversations/{member_id}` - Get conversations with filtering
- `GET /journey/decisions/{member_id}` - Get decisions with filtering
- `GET /journey/metrics/{member_id}` - Get member metrics
- `GET /journey/team-metrics/{member_id}` - Get team performance metrics
- `GET /journey/decision-context/{decision_id}` - Get decision context and conversations

## Data Flow

1. **Generation**: Local AI generates conversations for each month
2. **Parsing**: Conversations are parsed and structured
3. **Decision Creation**: AI analyzes conversations to create health decisions
4. **Event Generation**: Health events are created based on journey data
5. **Metrics Calculation**: Team hours and member metrics are calculated
6. **Storage**: All data is stored in the database
7. **Visualization**: Frontend displays data in interactive charts and timelines

## Customization

### Adding New Decision Types
- Update `_determine_decision_type()` in `journey_service.py`
- Add new decision types to the database model
- Update frontend icons and colors

### Modifying Conversation Generation
- Edit prompts in `local_ai_service.py`
- Adjust conversation parsing logic in `journey_service.py`
- Modify role determination and tagging

### Extending Metrics
- Add new fields to database models
- Update the metrics calculation logic
- Extend frontend dashboard components

## Benefits

1. **Zero API Costs**: 100% local AI generation
2. **Complete Traceability**: Every decision links back to conversations
3. **Rich Visualization**: Interactive timeline and metrics dashboard
4. **Data Persistence**: All data stored for analysis and compliance
5. **Scalable Architecture**: Easy to extend and customize

## Troubleshooting

### Ollama Issues
- Ensure Ollama is running: `ollama serve`
- Check model availability: `ollama list`
- Pull required model: `ollama pull llama2`

### Database Issues
- Run `python init_database.py` to recreate tables
- Check database connection in `database.py`
- Verify SQLite file permissions

### Frontend Issues
- Clear browser cache
- Check console for API errors
- Verify backend is running on port 8080

## Future Enhancements

1. **Real-time Updates**: WebSocket integration for live data
2. **Advanced Analytics**: Machine learning insights and predictions
3. **Export Functionality**: PDF reports and data export
4. **Multi-member Support**: Dashboard for multiple members
5. **Integration APIs**: Connect with external health systems

## Support

For issues or questions:
1. Check the console logs for error messages
2. Verify all dependencies are installed
3. Ensure Ollama is running and accessible
4. Check database connectivity and permissions
