from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    preferred_name = Column(String(100), nullable=False)
    dob = Column(String(10), nullable=False)  # YYYY-MM-DD format
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    residence = Column(String(100), nullable=False)
    travel_hubs = Column(JSON, nullable=False)  # List of travel locations
    occupation = Column(String(200), nullable=False)
    pa = Column(String(100), nullable=False)  # Personal Assistant
    tech_preferences = Column(JSON, nullable=False)  # Wearables, data sharing preferences
    health_goals = Column(JSON, nullable=False)  # List of health goals with targets
    communication_preferences = Column(JSON, nullable=False)  # Channel, response time, etc.
    scheduling_preferences = Column(JSON, nullable=False)  # Exercise times, weekly hours
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    conversations = relationship("Conversation", back_populates="member")
    health_events = relationship("HealthEvent", back_populates="member")
    decisions = relationship("Decision", back_populates="member")
    metrics = relationship("MemberMetrics", back_populates="member")
    team_metrics = relationship("TeamMetrics", back_populates="member")
    
    __table_args__ = (
        Index('idx_member_name', 'preferred_name'),
        Index('idx_member_residence', 'residence'),
    )

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String(50), primary_key=True, index=True)  # UUID-like ID
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    date = Column(String(10), nullable=False)  # YYYY-MM-DD format
    time = Column(String(5), nullable=False)  # HH:MM format
    sender = Column(String(100), nullable=False)  # Rohan or Elyx team member
    role = Column(String(100), nullable=False)  # member, doctor, coach, nutritionist, etc.
    text = Column(Text, nullable=False)
    tags = Column(JSON, nullable=False)  # List of tags for categorization
    relates_to = Column(String(50), nullable=True)  # ID of related message
    month = Column(Integer, nullable=True)  # Month number (1-8)
    week_number = Column(Integer, nullable=True)  # Week number within the journey
    travel_context = Column(String(200), nullable=True)  # Travel context for this period
    ai_generated = Column(Boolean, default=False)  # Whether this was AI-generated
    ai_model = Column(String(100), nullable=True)  # Which AI model generated it
    ai_prompt = Column(Text, nullable=True)  # The prompt used
    decision_impact = Column(JSON, nullable=True)  # List of decision IDs influenced by this message
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    member = relationship("Member", back_populates="conversations")
    
    __table_args__ = (
        Index('idx_conversation_date', 'date'),
        Index('idx_conversation_sender', 'sender'),
        Index('idx_conversation_tags', 'tags'),
        Index('idx_conversation_ai', 'ai_generated'),
        Index('idx_conversation_month_week', 'month', 'week_number'),
    )

class HealthEvent(Base):
    __tablename__ = "health_events"
    
    id = Column(String(50), primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    date = Column(String(10), nullable=False)
    event_type = Column(String(100), nullable=False)  # test, exercise_update, travel, etc.
    title = Column(String(200), nullable=False)
    details = Column(JSON, nullable=False)  # Event-specific details
    month = Column(Integer, nullable=True)  # Month number (1-8)
    week_number = Column(Integer, nullable=True)  # Week number within the journey
    linked_conversations = Column(JSON, nullable=False)  # List of conversation IDs
    linked_decisions = Column(JSON, nullable=False)  # List of decision IDs
    ai_generated = Column(Boolean, default=False)
    ai_context = Column(Text, nullable=True)  # AI reasoning for this event
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    member = relationship("Member", back_populates="health_events")
    
    __table_args__ = (
        Index('idx_event_date', 'date'),
        Index('idx_event_type', 'event_type'),
        Index('idx_event_ai', 'ai_generated'),
        Index('idx_event_month_week', 'month', 'week_number'),
    )

class Decision(Base):
    __tablename__ = "decisions"
    
    id = Column(String(50), primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    date = Column(String(10), nullable=False)
    title = Column(String(200), nullable=False)
    reason = Column(Text, nullable=False)
    decision_type = Column(String(100), nullable=False)  # medication, test, exercise, nutrition, etc.
    month = Column(Integer, nullable=True)  # Month number (1-8)
    week_number = Column(Integer, nullable=True)  # Week number within the journey
    triggered_by_conversation = Column(String(50), nullable=True)  # ID of conversation that triggered this
    supporting_conversations = Column(JSON, nullable=False)  # List of conversation IDs that support this decision
    effects = Column(JSON, nullable=False)  # List of event IDs affected
    ai_generated = Column(Boolean, default=False)
    ai_reasoning = Column(Text, nullable=True)  # AI's reasoning process
    confidence_score = Column(Float, nullable=True)  # AI confidence (0.0-1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    member = relationship("Member", back_populates="decisions")
    
    __table_args__ = (
        Index('idx_decision_date', 'date'),
        Index('idx_decision_ai', 'ai_generated'),
        Index('idx_decision_confidence', 'confidence_score'),
        Index('idx_decision_month_week', 'month', 'week_number'),
        Index('idx_decision_type', 'decision_type'),
    )

class MemberMetrics(Base):
    __tablename__ = "member_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    week_start = Column(String(10), nullable=False)
    week_end = Column(String(10), nullable=False)
    month = Column(Integer, nullable=True)  # Month number (1-8)
    week_number = Column(Integer, nullable=True)  # Week number within the journey
    adherence_estimate = Column(Float, nullable=False)  # 0.0-1.0
    hours_committed = Column(Float, nullable=False)
    key_events = Column(JSON, nullable=False)  # List of event IDs
    notes = Column(Text, nullable=True)
    ai_insights = Column(Text, nullable=True)  # AI-generated insights for the week
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    member = relationship("Member", back_populates="metrics")
    
    __table_args__ = (
        Index('idx_metrics_week', 'week_start', 'week_end'),
        Index('idx_metrics_adherence', 'adherence_estimate'),
        Index('idx_metrics_month_week', 'month', 'week_number'),
    )

class TeamMetrics(Base):
    __tablename__ = "team_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    date = Column(String(10), nullable=False)
    month = Column(Integer, nullable=True)  # Month number (1-8)
    week_number = Column(Integer, nullable=True)  # Week number within the journey
    doctor_hours = Column(Float, default=0.0)
    coach_hours = Column(Float, default=0.0)
    nutritionist_hours = Column(Float, default=0.0)
    physio_hours = Column(Float, default=0.0)
    concierge_hours = Column(Float, default=0.0)
    total_interventions = Column(Integer, default=0)
    linked_conversations = Column(JSON, nullable=False)  # List of conversation IDs that contributed to these hours
    ai_optimization_suggestions = Column(Text, nullable=True)  # AI suggestions for team efficiency
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    member = relationship("Member", back_populates="team_metrics")
    
    __table_args__ = (
        Index('idx_team_metrics_date', 'date'),
        Index('idx_team_metrics_member', 'member_id'),
        Index('idx_team_metrics_month_week', 'month', 'week_number'),
    )

class AIIntegration(Base):
    __tablename__ = "ai_integrations"
    
    id = Column(Integer, primary_key=True, index=True)
    integration_name = Column(String(100), nullable=False)  # openai, anthropic, etc.
    model_name = Column(String(100), nullable=False)  # gpt-4, claude-3, etc.
    api_key_hash = Column(String(255), nullable=False)  # Hashed API key
    is_active = Column(Boolean, default=True)
    rate_limit = Column(Integer, nullable=True)  # Requests per minute
    cost_per_token = Column(Float, nullable=True)  # Cost tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_used = Column(DateTime(timezone=True), nullable=True)
    
    __table_args__ = (
        Index('idx_ai_integration_name', 'integration_name'),
        Index('idx_ai_integration_active', 'is_active'),
    )

class AIPrompt(Base):
    __tablename__ = "ai_prompts"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_name = Column(String(100), nullable=False, unique=True)
    prompt_text = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)  # conversation, decision, insight, etc.
    variables = Column(JSON, nullable=False)  # Template variables
    ai_model = Column(String(100), nullable=True)  # Preferred model
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_prompt_name', 'prompt_name'),
        Index('idx_prompt_category', 'category'),
        Index('idx_prompt_active', 'is_active'),
    )

class AIGenerationLog(Base):
    __tablename__ = "ai_generation_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("ai_prompts.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    input_data = Column(JSON, nullable=False)  # Input context
    generated_output = Column(Text, nullable=False)
    ai_model = Column(String(100), nullable=False)
    tokens_used = Column(Integer, nullable=True)
    cost = Column(Float, nullable=True)
    generation_time = Column(Float, nullable=True)  # Seconds
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    member = relationship("Member")
    
    __table_args__ = (
        Index('idx_generation_log_date', 'created_at'),
        Index('idx_generation_log_member', 'member_id'),
        Index('idx_generation_log_success', 'success'),
    )
