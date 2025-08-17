from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.database import get_db
from app.services.journey_service import journey_service
from app.services.local_ai_service import local_ai_service
from app.models.database import Member, Conversation, Decision, HealthEvent, MemberMetrics, TeamMetrics
from app.models.schemas import JourneyData

router = APIRouter(prefix="/journey", tags=["journey"])

@router.post("/generate/{member_id}")
async def generate_journey(member_id: int, db: Session = Depends(get_db)):
    """Generate a complete 8-month journey for a member"""
    try:
        # Get member data
        member = db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # Convert member to dict
        member_data = {
            "id": member.id,
            "preferred_name": member.preferred_name,
            "age": member.age,
            "gender": member.gender,
            "residence": member.residence,
            "travel_hubs": member.travel_hubs,
            "occupation": member.occupation,
            "health_goals": member.health_goals
        }
        
        # Generate and store journey
        result = journey_service.generate_and_store_journey(member_data, db)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=f"Failed to generate journey: {result['error']}")
        
        return {
            "success": True,
            "message": "Journey generated and stored successfully",
            "data": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/timeline/{member_id}")
async def get_journey_timeline(member_id: int, db: Session = Depends(get_db)):
    """Get the complete journey timeline for visualization"""
    try:
        # Get all conversations
        conversations = db.query(Conversation).filter(
            Conversation.member_id == member_id
        ).order_by(Conversation.date, Conversation.time).all()
        
        # Get all decisions
        decisions = db.query(Decision).filter(
            Decision.member_id == member_id
        ).order_by(Decision.date).all()
        
        # Get all health events
        health_events = db.query(HealthEvent).filter(
            HealthEvent.member_id == member_id
        ).order_by(HealthEvent.date).all()
        
        # Get all metrics
        metrics = db.query(MemberMetrics).filter(
            MemberMetrics.member_id == member_id
        ).order_by(MemberMetrics.week_start).all()
        
        # Get team metrics
        team_metrics = db.query(TeamMetrics).filter(
            TeamMetrics.member_id == member_id
        ).order_by(TeamMetrics.date).all()
        
        # Build timeline data
        timeline_data = {
            "member_id": member_id,
            "conversations": [
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
            ],
            "decisions": [
                {
                    "id": d.id,
                    "date": d.date,
                    "title": d.title,
                    "reason": d.reason,
                    "decision_type": d.decision_type,
                    "month": d.month,
                    "week_number": d.week_number,
                    "triggered_by_conversation": d.triggered_by_conversation,
                    "supporting_conversations": d.supporting_conversations,
                    "effects": d.effects,
                    "confidence_score": d.confidence_score
                }
                for d in decisions
            ],
            "health_events": [
                {
                    "id": e.id,
                    "date": e.date,
                    "event_type": e.event_type,
                    "title": e.title,
                    "details": e.details,
                    "month": e.month,
                    "week_number": e.week_number,
                    "linked_conversations": e.linked_conversations,
                    "linked_decisions": e.linked_decisions
                }
                for e in health_events
            ],
            "metrics": [
                {
                    "week_start": m.week_start,
                    "week_end": m.week_end,
                    "month": m.month,
                    "week_number": m.week_number,
                    "adherence_estimate": m.adherence_estimate,
                    "hours_committed": m.hours_committed,
                    "key_events": m.key_events,
                    "notes": m.notes,
                    "ai_insights": m.ai_insights
                }
                for m in metrics
            ],
            "team_metrics": [
                {
                    "date": tm.date,
                    "month": tm.month,
                    "week_number": tm.week_number,
                    "doctor_hours": tm.doctor_hours,
                    "coach_hours": tm.coach_hours,
                    "nutritionist_hours": tm.nutritionist_hours,
                    "physio_hours": tm.physio_hours,
                    "concierge_hours": tm.concierge_hours,
                    "total_interventions": tm.total_interventions,
                    "linked_conversations": tm.linked_conversations
                }
                for tm in team_metrics
            ]
        }
        
        return {
            "success": True,
            "timeline": timeline_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{member_id}")
async def get_conversations(member_id: int, month: int = None, week: int = None, db: Session = Depends(get_db)):
    """Get conversations for a member with optional filtering"""
    try:
        query = db.query(Conversation).filter(Conversation.member_id == member_id)
        
        if month is not None:
            query = query.filter(Conversation.month == month)
        if week is not None:
            query = query.filter(Conversation.week_number == week)
        
        conversations = query.order_by(Conversation.date, Conversation.time).all()
        
        return {
            "success": True,
            "conversations": [
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

@router.get("/decisions/{member_id}")
async def get_decisions(member_id: int, month: int = None, decision_type: str = None, db: Session = Depends(get_db)):
    """Get decisions for a member with optional filtering"""
    try:
        query = db.query(Decision).filter(Decision.member_id == member_id)
        
        if month is not None:
            query = query.filter(Decision.month == month)
        if decision_type is not None:
            query = query.filter(Decision.decision_type == decision_type)
        
        decisions = query.order_by(Decision.date).all()
        
        return {
            "success": True,
            "decisions": [
                {
                    "id": d.id,
                    "date": d.date,
                    "title": d.title,
                    "reason": d.reason,
                    "decision_type": d.decision_type,
                    "month": d.month,
                    "week_number": d.week_number,
                    "triggered_by_conversation": d.triggered_by_conversation,
                    "supporting_conversations": d.supporting_conversations,
                    "effects": d.effects,
                    "confidence_score": d.confidence_score
                }
                for d in decisions
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/{member_id}")
async def get_metrics(member_id: int, month: int = None, db: Session = Depends(get_db)):
    """Get metrics for a member with optional filtering"""
    try:
        query = db.query(MemberMetrics).filter(MemberMetrics.member_id == member_id)
        
        if month is not None:
            query = query.filter(MemberMetrics.month == month)
        
        metrics = query.order_by(MemberMetrics.week_start).all()
        
        return {
            "success": True,
            "metrics": [
                {
                    "week_start": m.week_start,
                    "week_end": m.week_end,
                    "month": m.month,
                    "week_number": m.week_number,
                    "adherence_estimate": m.adherence_estimate,
                    "hours_committed": m.hours_committed,
                    "key_events": m.key_events,
                    "notes": m.notes,
                    "ai_insights": m.ai_insights
                }
                for m in metrics
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/team-metrics/{member_id}")
async def get_team_metrics(member_id: int, month: int = None, db: Session = Depends(get_db)):
    """Get team metrics for a member with optional filtering"""
    try:
        query = db.query(TeamMetrics).filter(TeamMetrics.member_id == member_id)
        
        if month is not None:
            query = query.filter(TeamMetrics.month == month)
        
        team_metrics = query.order_by(TeamMetrics.date).all()
        
        return {
            "success": True,
            "team_metrics": [
                {
                    "date": tm.date,
                    "month": tm.month,
                    "week_number": tm.week_number,
                    "doctor_hours": tm.doctor_hours,
                    "coach_hours": tm.coach_hours,
                    "nutritionist_hours": tm.nutritionist_hours,
                    "physio_hours": tm.physio_hours,
                    "concierge_hours": tm.concierge_hours,
                    "total_interventions": tm.total_interventions,
                    "linked_conversations": tm.linked_conversations
                }
                for tm in team_metrics
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/decision-context/{decision_id}")
async def get_decision_context(decision_id: str, db: Session = Depends(get_db)):
    """Get the context and conversations that led to a specific decision"""
    try:
        # Get the decision
        decision = db.query(Decision).filter(Decision.id == decision_id).first()
        if not decision:
            raise HTTPException(status_code=404, detail="Decision not found")
        
        # Get supporting conversations
        supporting_conversations = []
        if decision.supporting_conversations:
            conversations = db.query(Conversation).filter(
                Conversation.id.in_(decision.supporting_conversations)
            ).order_by(Conversation.date, Conversation.time).all()
            
            supporting_conversations = [
                {
                    "id": c.id,
                    "date": c.date,
                    "time": c.time,
                    "sender": c.sender,
                    "role": c.role,
                    "text": c.text,
                    "tags": c.tags
                }
                for c in conversations
            ]
        
        # Get triggered conversation
        triggered_conversation = None
        if decision.triggered_by_conversation:
            conv = db.query(Conversation).filter(Conversation.id == decision.triggered_by_conversation).first()
            if conv:
                triggered_conversation = {
                    "id": conv.id,
                    "date": conv.date,
                    "time": conv.time,
                    "sender": conv.sender,
                    "role": conv.role,
                    "text": conv.text,
                    "tags": conv.tags
                }
        
        return {
            "success": True,
            "decision": {
                "id": decision.id,
                "date": decision.date,
                "title": decision.title,
                "reason": decision.reason,
                "decision_type": decision.decision_type,
                "month": decision.month,
                "week_number": decision.week_number,
                "confidence_score": decision.confidence_score,
                "ai_reasoning": decision.ai_reasoning
            },
            "triggered_conversation": triggered_conversation,
            "supporting_conversations": supporting_conversations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
