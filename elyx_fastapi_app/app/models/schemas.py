from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Message(BaseModel):
    id: str
    date: str
    time: str
    sender: str
    role: str
    text: str
    tags: List[str] = []
    relates_to: Optional[str] = None  # message id it responds to
    month: Optional[int] = None
    week_number: Optional[int] = None
    travel_context: Optional[str] = None
    decision_impact: Optional[List[str]] = None

class Decision(BaseModel):
    id: str
    date: str
    title: str
    reason: str
    decision_type: str
    month: Optional[int] = None
    week_number: Optional[int] = None
    triggered_by_message: Optional[str] = None  # message id
    supporting_conversations: List[str] = []
    effects: List[str] = []  # ids of interventions/tests/exercises
    confidence_score: Optional[float] = None

class Event(BaseModel):
    id: str
    date: str
    type: str  # 'test', 'exercise_update', 'travel', 'report', 'medication', 'therapy'
    title: str
    details: Dict[str, Any] = {}
    month: Optional[int] = None
    week_number: Optional[int] = None
    links: List[str] = [] # message/decision ids providing traceability

class WeekSummary(BaseModel):
    week_start: str
    week_end: str
    month: Optional[int] = None
    week_number: Optional[int] = None
    adherence_estimate: float
    hours_committed: float
    key_events: List[str] = []  # event ids
    notes: Optional[str] = None

class Timeline(BaseModel):
    start_date: str
    end_date: str
    months: List[Dict[str, Any]] = []
    weeks: List[WeekSummary]
    events: List[Event]
    decisions: List[Decision]
    messages: List[Message]

class TeamMetrics(BaseModel):
    date: str
    month: Optional[int] = None
    week_number: Optional[int] = None
    doctor_hours: float = 0
    coach_hours: float = 0
    nutritionist_hours: float = 0
    physio_hours: float = 0
    concierge_hours: float = 0
    total_interventions: int = 0
    linked_conversations: List[str] = []

class Goal(BaseModel):
    goal: str
    target: str

class TechPreferences(BaseModel):
    wearables: List[str]
    considering: List[str]
    share_data: bool

class Preferences(BaseModel):
    channel: str
    response_time: str
    detail_depth: str
    language: str

class Scheduling(BaseModel):
    morning_exercise: bool
    avg_weekly_hours: int
    travels_every_2_weeks: bool

class Persona(BaseModel):
    preferred_name: str = "Rohan Patel"
    dob: str = "1979-03-12"
    age: int = 46
    gender: str = "Male"
    residence: str = "Singapore"
    travel_hubs: List[str] = ["UK", "US", "South Korea", "Jakarta"]
    occupation: str = "Regional Head of Sales for a FinTech company"
    pa: str = "Sarah Tan"
    tech: TechPreferences
    goals: List[Goal]
    preferences: Preferences
    scheduling: Scheduling

class ConversationResponse(BaseModel):
    id: str
    date: str
    time: str
    sender: str
    role: str
    text: str
    tags: List[str]
    month: Optional[int]
    week_number: Optional[int]
    travel_context: Optional[str]
    decision_impact: Optional[List[str]]

class DecisionResponse(BaseModel):
    id: str
    date: str
    title: str
    reason: str
    decision_type: str
    month: Optional[int]
    week_number: Optional[int]
    triggered_by_conversation: Optional[str]
    supporting_conversations: List[str]
    effects: List[str]
    confidence_score: Optional[float]

class JourneyData(BaseModel):
    member_id: int
    generated_at: str
    episodes: List[Dict[str, Any]]
    total_conversations: int
    travel_events: List[Dict[str, Any]]
    diagnostic_tests: List[Dict[str, Any]]
    plan_modifications: List[Dict[str, Any]]
