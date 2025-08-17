import os
import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.database import (
    Member, Conversation, HealthEvent, Decision, 
    MemberMetrics, TeamMetrics, AIPrompt, AIGenerationLog
)
from app.services.local_ai_service import local_ai_service

class JourneyService:
    def __init__(self):
        self.local_ai = local_ai_service
    
    def generate_and_store_journey(self, member_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """Generate complete 8-month journey and store in database"""
        try:
            print(f"🚀 Generating journey for member {member_data.get('id')}")
            
            # Generate the journey using local AI
            journey_result = self.local_ai.generate_8_month_journey(member_data)
            
            if not journey_result["success"]:
                raise ValueError(f"Failed to generate journey: {journey_result['error']}")
            
            journey_data = journey_result["journey_data"]
            
            # Parse and store conversations
            conversations = self._parse_conversations_from_journey(journey_data, member_data["id"])
            stored_conversations = self._store_conversations(conversations, db)
            
            # Generate and store decisions
            decisions = self._generate_decisions_from_conversations(stored_conversations, member_data, db)
            
            # Generate and store health events
            health_events = self._generate_health_events_from_journey(journey_data, stored_conversations, decisions, member_data["id"])
            self._store_health_events(health_events, db)
            
            # Generate and store metrics
            metrics = self._generate_metrics_from_journey(journey_data, stored_conversations, decisions, member_data["id"])
            self._store_metrics(metrics, db)
            
            # Generate and store team metrics
            team_metrics = self._generate_team_metrics_from_conversations(stored_conversations, member_data["id"])
            self._store_team_metrics(team_metrics, db)
            
            print(f"✅ Journey generated and stored successfully")
            
            return {
                "success": True,
                "journey_data": journey_data,
                "conversations_stored": len(stored_conversations),
                "decisions_stored": len(decisions),
                "health_events_stored": len(health_events),
                "metrics_stored": len(metrics)
            }
            
        except Exception as e:
            print(f"❌ Error generating journey: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_conversations_from_journey(self, journey_data: Dict[str, Any], member_id: int) -> List[Dict[str, Any]]:
        """Parse conversations from the generated journey data"""
        conversations = []
        
        for episode in journey_data.get("episodes", []):
            month = episode.get("month", 1)
            week_start = episode.get("week_start", 1)
            travel_context = episode.get("travel_context", "")
            
            # Parse the generated conversations text
            episode_conversations = episode.get("conversations", "")
            parsed_convos = self._parse_conversation_text(episode_conversations, month, week_start, travel_context)
            
            for convo in parsed_convos:
                convo["member_id"] = member_id
                convo["month"] = month
                convo["week_number"] = week_start
                convo["travel_context"] = travel_context
                conversations.append(convo)
        
        return conversations
    
    def _parse_conversation_text(self, conversation_text: str, month: int, week_start: int, travel_context: str) -> List[Dict[str, Any]]:
        """Parse the AI-generated conversation text into structured conversations"""
        conversations = []
        
        # Split by lines and parse each message
        lines = conversation_text.split('\n')
        current_date = datetime.now() - timedelta(days=(8-month)*30)
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or len(line) < 10:
                continue
            
            # Parse sender and message
            if ':' in line:
                sender_part, message_part = line.split(':', 1)
                sender = sender_part.strip()
                message = message_part.strip()
                
                # Determine role based on sender
                role = self._determine_role(sender)
                
                # Generate realistic date and time
                message_date = current_date + timedelta(days=i//2, hours=i%12)
                
                conversation = {
                    "id": str(uuid.uuid4()),
                    "date": message_date.strftime("%Y-%m-%d"),
                    "time": message_date.strftime("%H:%M"),
                    "sender": sender,
                    "role": role,
                    "text": message,
                    "tags": self._generate_tags_for_message(message, month, week_start),
                    "relates_to": None,
                    "ai_generated": True,
                    "ai_model": "groq",
                    "ai_prompt": f"episode_{month}_conversation",
                    "decision_impact": []
                }
                
                conversations.append(conversation)
        
        return conversations
    
    def _determine_role(self, sender: str) -> str:
        """Determine the role of the sender"""
        sender_lower = sender.lower()
        
        if "rohan" in sender_lower or "patel" in sender_lower:
            return "member"
        elif "dr." in sender_lower or "warren" in sender_lower:
            return "doctor"
        elif "ruby" in sender_lower:
            return "concierge"
        elif "carla" in sender_lower:
            return "nutritionist"
        elif "rachel" in sender_lower:
            return "coach"
        elif "advik" in sender_lower:
            return "data_analyst"
        elif "neel" in sender_lower:
            return "strategist"
        else:
            return "team_member"
    
    def _generate_tags_for_message(self, message: str, month: int, week_start: int) -> List[str]:
        """Generate tags for message categorization"""
        tags = []
        message_lower = message.lower()
        
        # Month-based tags
        tags.append(f"month_{month}")
        tags.append(f"week_{week_start}")
        
        # Content-based tags
        if any(word in message_lower for word in ["test", "diagnostic", "panel"]):
            tags.extend(["diagnostic", "medical"])
        if any(word in message_lower for word in ["exercise", "workout", "training"]):
            tags.extend(["exercise", "fitness"])
        if any(word in message_lower for word in ["nutrition", "diet", "food"]):
            tags.extend(["nutrition", "diet"])
        if any(word in message_lower for word in ["travel", "trip", "flight"]):
            tags.extend(["travel", "scheduling"])
        if any(word in message_lower for word in ["progress", "improvement", "results"]):
            tags.extend(["progress", "results"])
        
        return tags
    
    def _store_conversations(self, conversations: List[Dict[str, Any]], db: Session) -> List[Dict[str, Any]]:
        """Store conversations in the database"""
        stored_conversations = []
        
        for convo_data in conversations:
            try:
                # Create conversation object
                conversation = Conversation(**convo_data)
                db.add(conversation)
                db.commit()
                db.refresh(conversation)
                
                stored_conversations.append(convo_data)
                
            except Exception as e:
                print(f"⚠️  Failed to store conversation: {e}")
                db.rollback()
                continue
        
        return stored_conversations
    
    def _generate_decisions_from_conversations(self, conversations: List[Dict[str, Any]], 
                                            member_data: Dict[str, Any], db: Session) -> List[Dict[str, Any]]:
        """Generate decisions based on conversations"""
        decisions = []
        
        print(f"🔍 Generating decisions from {len(conversations)} conversations...")
        
        # Group conversations by month and week
        conversations_by_period = {}
        for convo in conversations:
            key = (convo["month"], convo["week_number"])
            if key not in conversations_by_period:
                conversations_by_period[key] = []
            conversations_by_period[key].append(convo)
        
        print(f"📅 Found {len(conversations_by_period)} conversation periods")
        
        # Generate decisions for each period
        for (month, week), period_conversations in conversations_by_period.items():
            print(f"🤖 Generating decision for Month {month} Week {week}...")
            
            # Generate health decisions using local AI
            decision_result = self.local_ai.generate_health_decision(
                member_data, period_conversations, {"month": month, "week": week}
            )
            
            if decision_result["success"]:
                decision_data = {
                    "id": str(uuid.uuid4()),
                    "member_id": member_data["id"],
                    "date": period_conversations[0]["date"],
                    "title": f"Month {month} Week {week} Health Decision",
                    "reason": decision_result["decision"],
                    "decision_type": self._determine_decision_type(period_conversations),
                    "month": month,
                    "week_number": week,
                    "triggered_by_conversation": period_conversations[0]["id"],
                    "supporting_conversations": [c["id"] for c in period_conversations],
                    "effects": [],
                    "ai_generated": True,
                    "ai_reasoning": decision_result.get("reasoning", ""),
                    "confidence_score": decision_result.get("confidence_score", 0.85)
                }
                
                # Store decision
                try:
                    decision = Decision(**decision_data)
                    db.add(decision)
                    db.commit()
                    db.refresh(decision)
                    
                    decisions.append(decision_data)
                    print(f"✅ Decision stored for Month {month} Week {week}")
                    
                    # Update conversations with decision impact
                    for convo in period_conversations:
                        if convo.get("decision_impact") is None:
                            convo["decision_impact"] = []
                        convo["decision_impact"].append(decision_data["id"])
                    
                except Exception as e:
                    print(f"⚠️  Failed to store decision: {e}")
                    db.rollback()
                    continue
            else:
                print(f"⚠️  Failed to generate decision for Month {month} Week {week}: {decision_result.get('error', 'Unknown error')}")
                # Create a simple fallback decision
                fallback_decision = {
                    "id": str(uuid.uuid4()),
                    "member_id": member_data["id"],
                    "date": period_conversations[0]["date"],
                    "title": f"Month {month} Week {week} Health Decision",
                    "reason": f"Health optimization decision based on {len(period_conversations)} conversations",
                    "decision_type": self._determine_decision_type(period_conversations),
                    "month": month,
                    "week_number": week,
                    "triggered_by_conversation": period_conversations[0]["id"],
                    "supporting_conversations": [c["id"] for c in period_conversations],
                    "effects": [],
                    "ai_generated": False,
                    "ai_reasoning": "Fallback decision due to AI generation failure",
                    "confidence_score": 0.5
                }
                
                try:
                    decision = Decision(**fallback_decision)
                    db.add(decision)
                    db.commit()
                    db.refresh(decision)
                    
                    decisions.append(fallback_decision)
                    print(f"✅ Fallback decision stored for Month {month} Week {week}")
                    
                except Exception as e:
                    print(f"⚠️  Failed to store fallback decision: {e}")
                    db.rollback()
                    continue
        
        print(f"🎯 Generated {len(decisions)} decisions total")
        return decisions
    
    def _determine_decision_type(self, conversations: List[Dict[str, Any]]) -> str:
        """Determine the type of decision based on conversations"""
        all_text = " ".join([c["text"].lower() for c in conversations])
        
        if any(word in all_text for word in ["test", "diagnostic", "panel"]):
            return "diagnostic_test"
        elif any(word in all_text for word in ["exercise", "workout", "training"]):
            return "exercise_plan"
        elif any(word in all_text for word in ["nutrition", "diet", "food"]):
            return "nutrition_plan"
        elif any(word in all_text for word in ["medication", "supplement", "vitamin"]):
            return "medication"
        else:
            return "general_health"
    
    def _generate_health_events_from_journey(self, journey_data: Dict[str, Any], 
                                           conversations: List[Dict[str, Any]], 
                                           decisions: List[Dict[str, Any]], 
                                           member_id: int) -> List[Dict[str, Any]]:
        """Generate health events from the journey data"""
        events = []
        
        # Diagnostic tests
        for test in journey_data.get("diagnostic_tests", []):
            event_data = {
                "id": str(uuid.uuid4()),
                "member_id": member_id,
                "date": self._calculate_date_for_month_week(test["month"], test["week"]),
                "event_type": "diagnostic_test",
                "title": f"Month {test['month']} Diagnostic Panel",
                "details": {
                    "month": test["month"],
                    "week": test["week"],
                    "type": test["type"],
                    "description": "Comprehensive health assessment"
                },
                "month": test["month"],
                "week_number": test["week"],
                "linked_conversations": [c["id"] for c in conversations if c["month"] == test["month"]],
                "linked_decisions": [d["id"] for d in decisions if d["month"] == test["month"]],
                "ai_generated": True,
                "ai_context": "Scheduled diagnostic test based on journey timeline"
            }
            events.append(event_data)
        
        # Plan modifications
        for mod in journey_data.get("plan_modifications", []):
            event_data = {
                "id": str(uuid.uuid4()),
                "member_id": member_id,
                "date": self._calculate_date_for_month_week(mod["month"], mod["week"]),
                "event_type": "plan_modification",
                "title": f"Month {mod['month']} Plan Update",
                "details": {
                    "month": mod["month"],
                    "week": mod["week"],
                    "reason": mod["reason"],
                    "description": "Health plan optimization"
                },
                "month": mod["month"],
                "week_number": mod["week"],
                "linked_conversations": [c["id"] for c in conversations if c["month"] == mod["month"]],
                "linked_decisions": [d["id"] for d in decisions if d["month"] == mod["month"]],
                "ai_generated": True,
                "ai_context": "Plan modification based on progress and travel constraints"
            }
            events.append(event_data)
        
        return events
    
    def _calculate_date_for_month_week(self, month: int, week: int) -> str:
        """Calculate date for a specific month and week"""
        base_date = datetime.now() - timedelta(days=(8-month)*30)
        week_date = base_date + timedelta(days=(week-1)*7)
        return week_date.strftime("%Y-%m-%d")
    
    def _store_health_events(self, events: List[Dict[str, Any]], db: Session):
        """Store health events in the database"""
        for event_data in events:
            try:
                event = HealthEvent(**event_data)
                db.add(event)
                db.commit()
            except Exception as e:
                print(f"⚠️  Failed to store health event: {e}")
                db.rollback()
                continue
    
    def _generate_metrics_from_journey(self, journey_data: Dict[str, Any], 
                                     conversations: List[Dict[str, Any]], 
                                     decisions: List[Dict[str, Any]], 
                                     member_id: int) -> List[Dict[str, Any]]:
        """Generate member metrics from the journey"""
        metrics = []
        
        for episode in journey_data.get("episodes", []):
            month = episode.get("month", 1)
            week_start = episode.get("week_start", 1)
            
            # Calculate adherence based on month (realistic pattern)
            adherence = max(0.3, min(0.9, 0.5 + (month - 1) * 0.05))
            
            metric_data = {
                "member_id": member_id,
                "week_start": self._calculate_date_for_month_week(month, week_start),
                "week_end": self._calculate_date_for_month_week(month, week_start + 3),
                "month": month,
                "week_number": week_start,
                "adherence_estimate": adherence,
                "hours_committed": adherence * 10,  # 10 hours per week target
                "key_events": [c["id"] for c in conversations if c["month"] == month],
                "notes": f"Month {month} progress tracking",
                "ai_insights": f"Adherence pattern shows {adherence:.1%} commitment level"
            }
            metrics.append(metric_data)
        
        return metrics
    
    def _store_metrics(self, metrics: List[Dict[str, Any]], db: Session):
        """Store metrics in the database"""
        for metric_data in metrics:
            try:
                metric = MemberMetrics(**metric_data)
                db.add(metric)
                db.commit()
            except Exception as e:
                print(f"⚠️  Failed to store metric: {e}")
                db.rollback()
                continue
    
    def _generate_team_metrics_from_conversations(self, conversations: List[Dict[str, Any]], 
                                                member_id: int) -> List[Dict[str, Any]]:
        """Generate team metrics from conversations"""
        team_metrics = []
        
        # Group by month and week
        conversations_by_period = {}
        for convo in conversations:
            key = (convo["month"], convo["week_number"])
            if key not in conversations_by_period:
                conversations_by_period[key] = []
            conversations_by_period[key].append(convo)
        
        for (month, week), period_conversations in conversations_by_period.items():
            # Calculate hours based on role and message count
            role_hours = {
                "doctor": 0.0,
                "coach": 0.0,
                "nutritionist": 0.0,
                "physio": 0.0,
                "concierge": 0.0
            }
            
            for convo in period_conversations:
                role = convo["role"]
                if role in role_hours:
                    role_hours[role] += 0.25  # 15 minutes per message
            
            metric_data = {
                "member_id": member_id,
                "date": period_conversations[0]["date"],
                "month": month,
                "week_number": week,
                "doctor_hours": role_hours["doctor"],
                "coach_hours": role_hours["coach"],
                "nutritionist_hours": role_hours["nutritionist"],
                "physio_hours": role_hours["physio"],
                "concierge_hours": role_hours["concierge"],
                "total_interventions": len(period_conversations),
                "linked_conversations": [c["id"] for c in period_conversations],
                "ai_optimization_suggestions": "Team coordination optimized for member's travel schedule"
            }
            team_metrics.append(metric_data)
        
        return team_metrics
    
    def _store_team_metrics(self, team_metrics: List[Dict[str, Any]], db: Session):
        """Store team metrics in the database"""
        for metric_data in team_metrics:
            try:
                metric = TeamMetrics(**metric_data)
                db.add(metric)
                db.commit()
            except Exception as e:
                print(f"⚠️  Failed to store team metric: {e}")
                db.rollback()
                continue

# Global journey service instance
journey_service = JourneyService()
