from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.routes import journey
from app.database import get_db, create_tables
from app.services.local_ai_service import local_ai_service
from app.services.journey_service import journey_service
from datetime import datetime

# Create tables on startup
create_tables()

app = FastAPI(
    title="Elyx Life – Member Journey API",
    version="2.0.0",
    description="Generates 8 months of WhatsApp-style communication, builds a member journey timeline, and tracks internal metrics with FREE local AI integration."
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(journey.router, prefix="/journey", tags=["Journey"])

@app.get("/", tags=["Root"])
def root():
    return {
        "service": "elyx-life-journey",
        "version": "2.0.0",
        "features": [
            "FREE Groq AI-powered conversation generation",
            "Database-backed data persistence",
            "Groq LLM integration",
            "Advanced health decision tracking",
            "Episode-based journey generation",
            "Fast AI inference with rate limiting"
        ],
        "endpoints": [
            "/journey/generate/{member_id}",
            "/journey/timeline/{member_id}", 
            "/journey/conversations/{member_id}",
            "/journey/decisions/{member_id}",
            "/journey/metrics/{member_id}",
            "/journey/team-metrics/{member_id}",
            "/journey/decision-context/{decision_id}",
            "/ai/models",
            "/ai/health"
        ],
    }

@app.get("/conversations/{member_id}", tags=["Conversations"])
def get_conversations(member_id: int, month: int = None, week: int = None, db: Session = Depends(get_db)):
    """Get conversations for a member with optional filtering"""
    try:
        from app.models.database import Conversation
        
        query = db.query(Conversation).filter(Conversation.member_id == member_id)
        
        if month is not None:
            query = query.filter(Conversation.month == month)
        if week is not None:
            query = query.filter(Conversation.week_number == week)
        
        conversations = query.order_by(Conversation.date, Conversation.time).all()
        
        return {
            "success": True,
            "items": [
                {
                    "id": c.id,
                    "date": c.date,
                    "time": c.time,
                    "sender": c.sender,
                    "role": c.role,
                    "text": c.text,
                    "tags": c.tags,
                    "month": c.month,
                    "week_number": c.week_number,
                    "travel_context": c.travel_context,
                    "decision_impact": c.decision_impact or []
                }
                for c in conversations
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test-conversations/{member_id}", tags=["Test"])
def test_conversations(member_id: int, db: Session = Depends(get_db)):
    """Test endpoint to check if conversations are being retrieved"""
    try:
        from app.models.database import Conversation
        
        conversations = db.query(Conversation).filter(Conversation.member_id == member_id).all()
        
        return {
            "success": True,
            "member_id": member_id,
            "conversation_count": len(conversations),
            "sample_conversation": {
                "id": conversations[0].id,
                "text": conversations[0].text[:100] if conversations else "No conversations",
                "date": conversations[0].date if conversations else None
            } if conversations else None
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "member_id": member_id
        }
    

@app.post("/generate-complete-journey", tags=["Journey Generation"])
def generate_complete_journey(db: Session = Depends(get_db)):
    """Generate complete 8-month journey with episode-specific conversations"""
    try:
        from app.models.database import Member
        
        # Get member data
        member = db.query(Member).first()
        if not member:
            raise HTTPException(status_code=404, detail="No member found in database")
        
        if not local_ai_service.groq_api_key:
            raise HTTPException(status_code=503, detail="Groq AI service not available. Please check your API key.")
        
        # Generate and store complete journey
        member_data = {
            "id": member.id,
            "preferred_name": member.preferred_name,
            "age": member.age,
            "occupation": member.occupation,
            "residence": member.residence,
            "travel_hubs": member.travel_hubs,
            "tech_preferences": member.tech_preferences,
            "health_goals": member.health_goals,
            "communication_preferences": member.communication_preferences,
            "scheduling_preferences": member.scheduling_preferences
        }
        
        result = journey_service.generate_and_store_journey(member_data, db)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=f"Journey generation failed: {result['error']}")
        
        return {
            "message": "Complete 8-month journey generated and stored successfully",
            "journey_data": result["journey_data"],
            "storage_summary": {
                "conversations_stored": result["conversations_stored"],
                "decisions_stored": result["decisions_stored"],
                "health_events_stored": result["health_events_stored"],
                "metrics_stored": result["metrics_stored"]
            },
            "ai_model": "groq",
            "local_model": False,
            "cost": "Free tier (rate limited)",
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Journey generation failed: {str(e)}")

@app.get("/ai/models", tags=["AI"])
def get_ai_models():
    """Get available AI models"""
    return {
        "available_models": local_ai_service.get_available_models(),
        "local_model": False,
        "cost": "Free tier (rate limited)"
    }

@app.get("/ai/health", tags=["AI"])
def ai_health_check():
    """Check health of Groq AI models"""
    return local_ai_service.health_check()

@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    # Check AI service health
    ai_health = local_ai_service.health_check()
    
    return {
        "status": "healthy",
        "database": db_status,
        "ai_service": "available" if ai_health["groq"] else "unavailable",
        "ai_models": ai_health["models_available"],
        "local_models": False,
        "cost": "Free tier (rate limited)",
        "timestamp": "2025-01-15T00:00:00Z"
    }
