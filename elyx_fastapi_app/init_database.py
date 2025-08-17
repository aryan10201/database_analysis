#!/usr/bin/env python3
"""
Database initialization script for Elyx Life Member Journey API
This script creates the database, tables, and seeds initial data.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent))

from app.database import SessionLocal, engine
from app.models.database import (
    Base, Member, AIPrompt, AIIntegration
)
from sqlalchemy import text

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database with sample data"""
    try:
        # Create tables using the correct Base
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        # Create a sample member
        db = next(get_db())
        
        # Check if member already exists
        existing_member = db.query(Member).first()
        if existing_member:
            print(f"✅ Member already exists: {existing_member.preferred_name}")
            return
        
        # Create sample member data
        sample_member = Member(
            preferred_name="Rohan Patel",
            dob="1979-03-12",
            age=46,
            gender="Male",
            residence="Singapore",
            travel_hubs=["UK", "US", "South Korea", "Jakarta"],
            occupation="Regional Head of Sales for a FinTech company",
            pa="Sarah Tan",
            tech_preferences={
                "wearables": ["Garmin Fenix 7", "Oura Ring"],
                "considering": ["Apple Watch Ultra"],
                "share_data": True
            },
            health_goals=[
                {"goal": "Improve cardiovascular health", "target": "Reduce resting heart rate by 10%"},
                {"goal": "Enhance cognitive performance", "target": "Improve focus and mental clarity"},
                {"goal": "Annual full-body screening", "target": "November 2025"}
            ],
            communication_preferences={
                "channel": "WhatsApp",
                "response_time": "Within 2 hours",
                "detail_depth": "Comprehensive",
                "language": "English"
            },
            scheduling_preferences={
                "morning_exercise": True,
                "avg_weekly_hours": 8,
                "travels_every_2_weeks": True
            }
        )
        
        db.add(sample_member)
        db.commit()
        db.refresh(sample_member)
        
        print(f"✅ Sample member created: {sample_member.preferred_name} (ID: {sample_member.id})")
        print("✅ Database initialization completed successfully")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)

def seed_initial_data():
    """Seed the database with initial data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_member = db.query(Member).first()
        if existing_member:
            print("⚠️  Database already contains data, skipping seeding...")
            return
        
        # Create Rohan Patel member
        print("👤 Creating member profile...")
        member = Member(
            preferred_name=PERSONA["preferred_name"],
            dob=PERSONA["dob"],
            age=PERSONA["age"],
            gender=PERSONA["gender"],
            residence=PERSONA["residence"],
            travel_hubs=PERSONA["travel_hubs"],
            occupation=PERSONA["occupation"],
            pa=PERSONA["pa"],
            tech_preferences=PERSONA["tech"],
            health_goals=PERSONA["goals"],
            communication_preferences=PERSONA["preferences"],
            scheduling_preferences=PERSONA["scheduling"]
        )
        db.add(member)
        db.flush()  # Get the ID
        
        # Create AI prompts
        print("🤖 Creating AI prompts...")
        ai_prompts = [
            AIPrompt(
                prompt_name="conversation_generation",
                prompt_text="""Generate a realistic WhatsApp-style conversation message for a health coaching scenario.

Member Profile: {member_profile}
Context: {context}

Requirements:
- Message should be conversational and natural
- Include appropriate emojis and casual language
- Should be relevant to the member's health goals
- Consider their travel schedule and preferences
- Make it sound like a real person, not AI-generated

Generate a single message that fits the context.""",
                description="Generate realistic conversation messages for health coaching",
                category="conversation",
                variables=["member_profile", "context"],
                ai_model="ollama",
                is_active=True
            ),
            AIPrompt(
                prompt_name="health_decision_generation",
                prompt_text="""Analyze the conversation history and health metrics to generate a health decision.

Member Profile: {member_profile}
Conversation History: {conversation_history}
Health Metrics: {health_metrics}

Requirements:
- Provide clear reasoning for the decision
- Consider member's adherence patterns
- Factor in travel and scheduling constraints
- Suggest specific actions or interventions
- Include confidence level and alternatives

Generate a structured decision with reasoning.""",
                description="Generate health decisions based on conversation history and metrics",
                category="decision",
                variables=["member_profile", "conversation_history", "health_metrics"],
                ai_model="ollama",
                is_active=True
            ),
            AIPrompt(
                prompt_name="weekly_insights_generation",
                prompt_text="""Generate weekly insights and recommendations based on the member's performance.

Member Profile: {member_profile}
Weekly Metrics: {weekly_metrics}

Requirements:
- Analyze adherence patterns and trends
- Identify areas for improvement
- Provide actionable recommendations
- Consider upcoming travel or events
- Include motivational elements
- Keep insights concise but comprehensive

Generate weekly insights and next steps.""",
                description="Generate weekly insights and recommendations",
                category="insight",
                variables=["member_profile", "weekly_metrics"],
                ai_model="ollama",
                is_active=True
            )
        ]
        
        for prompt in ai_prompts:
            db.add(prompt)
        
        # Create AI integration placeholder
        print("🔌 Creating AI integration placeholder...")
        ai_integration = AIIntegration(
            integration_name="ollama",
            model_name="llama2",
            api_key_hash="local_model",
            is_active=True
        )
        db.add(ai_integration)
        
        # Commit all changes
        db.commit()
        print(f"✅ Created member with ID: {member.id}")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def test_database_connection():
    """Test the database connection"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Elyx Life Database Initialization Tool")
    print("=" * 50)
    
    # Test connection first
    if not test_database_connection():
        print("❌ Cannot proceed without database connection")
        sys.exit(1)
    
    # Initialize database
    try:
        init_database()
        print("\n🎯 Next steps:")
        print("1. Install Ollama from https://ollama.ai/download")
        print("2. Start Ollama: ollama serve")
        print("3. Download model: ollama pull llama2")
        print("4. Run the FastAPI application")
        print("5. Access the API at http://localhost:8080")
        print("6. View API docs at http://localhost:8080/docs")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)
