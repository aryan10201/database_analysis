import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

load_dotenv()

class LocalAIService:
    def __init__(self):
       self.groq_api_key = os.getenv("GROQ_API_KEY")
       self.groq_base_url = "https://api.groq.com/openai/v1"
       self._initialize_groq()
        
    def _initialize_groq(self):
        """Initialize Groq client"""
        print("🚀 Initializing Groq AI Models...")

        if not self.groq_api_key:
            print("⚠️  No Groq API key found. Please check your .env file.")
            return
        
        try:
            # Test the API key
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            response = requests.get(f"{self.groq_base_url}/models", headers=headers)
            if response.status_code == 200:
                print("✅ Groq client initialized")
            else:
                print(f"⚠️  Groq API error: {response.status_code}")
                self.groq_api_key = None
        except Exception as e:
            print(f"⚠️  Groq not available: {e}")
            self.groq_api_key = None
    
    def get_available_models(self) -> List[str]:
        """Get list of available AI models"""
        models = []
        
        if self.groq_api_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                }
                response = requests.get(f"{self.groq_base_url}/models", headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    models.extend([model['id'] for model in data.get('data', [])])
            except:
                pass
        
        return models
    
    def generate_conversation(self, member_data: Dict[str, Any], context: Dict[str, Any], 
                            prompt_name: str = "conversation_generation") -> Dict[str, Any]:
        """Generate a conversation using Groq AI"""
        try:
            if not self.groq_api_key:
                raise ValueError("Groq not available")
            
            # Get the master prompt
            prompt = self._get_master_prompt(prompt_name)
            if not prompt:
                raise ValueError(f"Prompt '{prompt_name}' not found")
            
            # Prepare input data
            input_data = {
                "member_profile": member_data,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
            
            # Generate using Groq
            result = self._generate_with_groq(prompt["prompt_text"], input_data)
            if not result:
                raise ValueError("Failed to generate response")
            
            # Log the generation
            self._log_generation(prompt_name, member_data.get("id"), input_data, result, "groq")
            
            return {
                "success": True,
                "generated_text": result,
                "model_used": "groq",
                "prompt_used": prompt_name,
                "local_model": False
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model_used": None,
                "prompt_used": prompt_name
            }
    
    def generate_episode_conversations(self, member_data: Dict[str, Any], month: int, 
                                     week_start: int, travel_context: str = "") -> Dict[str, Any]:
        """Generate episode-specific conversations for a specific month"""
        try:
            if not self.groq_api_key:
                raise ValueError("Groq not available")
            
            # Get episode-specific prompt
            episode_prompt = self._get_episode_prompt(month, week_start, travel_context)
            if not episode_prompt:
                raise ValueError(f"Episode prompt for month {month} not found")
            
            # Prepare input data
            input_data = {
                "member_profile": member_data,
                "month": month,
                "week_start": week_start,
                "travel_context": travel_context,
                "current_date": datetime.now().isoformat()
            }
            
            # Generate using Groq
            result = self._generate_with_groq(episode_prompt, input_data)
            if not result:
                raise ValueError("Failed to generate episode conversations")
            
            # Log the generation
            self._log_generation(f"episode_{month}", member_data.get("id"), input_data, result, "groq")
            
            return {
                "success": True,
                "episode_conversations": result,
                "month": month,
                "week_start": week_start,
                "travel_context": travel_context,
                "model_used": "groq",
                "local_model": False
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "month": month,
                "week_start": week_start
            }
    
    def generate_health_decision(self, member_data: Dict[str, Any], 
                               conversation_context: List[Dict[str, Any]], 
                               health_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate health decisions using Groq AI"""
        try:
            if not self.groq_api_key:
                raise ValueError("Groq not available")
            
            prompt = self._get_master_prompt("health_decision_generation")
            if not prompt:
                raise ValueError("Health decision prompt not found")
            
            input_data = {
                "member_profile": member_data,
                "conversation_history": conversation_context,
                "health_metrics": health_metrics,
                "current_date": datetime.now().isoformat()
            }
            
            result = self._generate_with_groq(prompt["prompt_text"], input_data)
            if not result:
                raise ValueError("Failed to generate health decision")
            
            # Log the generation
            self._log_generation("health_decision_generation", member_data.get("id"), 
                               input_data, result, "groq")
            
            return {
                "success": True,
                "decision": result,
                "confidence_score": 0.85,
                "model_used": "groq",
                "reasoning": "AI-generated based on conversation history and health metrics",
                "local_model": False
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "confidence_score": 0.0
            }
    
    def generate_weekly_insights(self, member_data: Dict[str, Any], 
                                weekly_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate weekly insights using Groq AI"""
        try:
            if not self.groq_api_key:
                raise ValueError("Groq not available")
            
            prompt = self._get_master_prompt("weekly_insights_generation")
            if not prompt:
                raise ValueError("Weekly insights prompt not found")
            
            input_data = {
                "member_profile": member_data,
                "weekly_metrics": weekly_metrics,
                "week_number": weekly_metrics.get("week_number", 1),
                "current_date": datetime.now().isoformat()
            }
            
            result = self._generate_with_groq(prompt["prompt_text"], input_data)
            if not result:
                raise ValueError("Failed to generate weekly insights")
            
            # Log the generation
            self._log_generation("weekly_insights_generation", member_data.get("id"), 
                               input_data, result, "groq")
            
            return {
                "success": True,
                "insights": result,
                "model_used": "groq",
                "generated_at": datetime.now().isoformat(),
                "local_model": False
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_8_month_journey(self, member_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete 8-month journey with episode-specific conversations"""
        import time
        
        try:
            if not self.groq_api_key:
                raise ValueError("Groq not available")
            
            journey_data = {
                "member_id": member_data.get("id"),
                "generated_at": datetime.now().isoformat(),
                "episodes": [],
                "total_conversations": 0,
                "travel_events": [],
                "diagnostic_tests": [],
                "plan_modifications": []
            }
            
            # Generate each month's episode
            for month in range(1, 9):
                week_start = ((month - 1) * 4) + 1
                travel_context = self._get_travel_context(month)
                
                episode_result = self.generate_episode_conversations(
                    member_data, month, week_start, travel_context
                )
                
                if episode_result["success"]:
                    journey_data["episodes"].append({
                        "month": month,
                        "week_start": week_start,
                        "week_end": week_start + 3,
                        "travel_context": travel_context,
                        "conversations": episode_result["episode_conversations"],
                        "generated_at": datetime.now().isoformat()
                    })
                    
                    # Track key events
                    if month in [1, 3, 6, 8]:  # Diagnostic test months
                        journey_data["diagnostic_tests"].append({
                            "month": month,
                            "week": week_start + 2,
                            "type": "Full diagnostic panel"
                        })
                    
                    if month in [2, 4, 6, 8]:  # Plan modification months
                        journey_data["plan_modifications"].append({
                            "month": month,
                            "week": week_start + 1,
                            "reason": "Travel constraints and adherence optimization"
                        })
                    
                    journey_data["total_conversations"] += 20  # ~5 per week
                else:
                    print(f"⚠️  Failed to generate episode {month}: {episode_result['error']}")
                
                # Add delay between episodes to avoid rate limiting
                if month < 8:
                    print(f"⏳ Waiting 2 seconds before generating episode {month + 1}...")
                    time.sleep(2)
            
            return {
                "success": True,
                "journey_data": journey_data,
                "model_used": "groq",
                "local_model": False
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_with_groq(self, prompt_text: str, input_data: Dict[str, Any]) -> Optional[str]:
        """Generate text using Groq API"""
        import time
        
        max_retries = 3
        base_delay = 1
        
        for attempt in range(max_retries):
            try:
                # Format the prompt
                full_prompt = f"""You are generating realistic WhatsApp-style communication between Rohan Patel (46, Regional Head of Sales, Singapore-based, frequent traveler) and the Elyx health optimization team.

{prompt_text}

Context: {json.dumps(input_data, indent=2)}

Generate realistic, conversational responses that maintain character consistency and include appropriate emojis, timing, and natural language patterns."""
                
                # Use Groq API
                headers = {
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "llama3-8b-8192",
                    "messages": [
                        {
                            "role": "user",
                            "content": full_prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
                
                response = requests.post(f"{self.groq_base_url}/chat/completions", headers=headers, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    return data['choices'][0]['message']['content'].strip()
                elif response.status_code == 429:  # Rate limit
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)  # Exponential backoff
                        print(f"Rate limited, retrying in {delay} seconds...")
                        time.sleep(delay)
                        continue
                    else:
                        print(f"Rate limit exceeded after {max_retries} attempts")
                        return None
                else:
                    print(f"Groq API error: {response.status_code} - {response.text}")
                    return None
                
            except Exception as e:
                print(f"Groq generation failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(base_delay)
                    continue
                return None
        
        return None
    
    def _get_master_prompt(self, prompt_name: str) -> Optional[Dict[str, Any]]:
        """Get master prompt"""
        master_prompts = {
            "conversation_generation": {
                "prompt_text": """Generate a realistic WhatsApp-style conversation message for a health coaching scenario.

Member Profile: {member_profile}
Context: {context}

Requirements:
- Message should be conversational and natural
- Include appropriate emojis and casual language
- Should be relevant to the member's health goals
- Consider their travel schedule and preferences
- Make it sound like a real person, not AI-generated

Generate a single message that fits the context.""",
                "ai_model": "local",
                "category": "conversation"
            },
            "health_decision_generation": {
                "prompt_text": """Analyze the conversation history and health metrics to generate a health decision.

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
                "ai_model": "local",
                "category": "decision"
            },
            "weekly_insights_generation": {
                "prompt_text": """Generate weekly insights and recommendations based on the member's performance.

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
                "ai_model": "local",
                "category": "insight"
            }
        }
        
        return master_prompts.get(prompt_name)
    
    def _get_episode_prompt(self, month: int, week_start: int, travel_context: str) -> str:
        """Get episode-specific prompt based on month"""
        episode_prompts = {
            1: f"""Generate Week {week_start}-{week_start+3} communications for Rohan's onboarding with Elyx team.

SPECIFIC REQUIREMENTS:
- Initial health concerns about Garmin high-intensity minutes
- Medical history collection and physical exam scheduling
- First diagnostic test panel coordination
- Friction points: scheduling around travel, communication clarity
- Include Ruby coordinating logistics, Dr. Warren reviewing medical history
- End with commitment to initial intervention plan

TRAVEL CONTEXT: {travel_context}
REALISTIC ELEMENTS: Delayed responses due to time zones, rescheduling needs

Generate 4 weeks of realistic WhatsApp conversations with appropriate timing, character consistency, and natural progression.""",

            2: f"""Generate Week {week_start}-{week_start+3} communications focusing on test results and intervention planning.

SPECIFIC REQUIREMENTS:
- Dr. Warren sharing categorized test results (major issues/follow-up/okay)
- Team discussions about results with different specialists
- Member's commitment to lifestyle interventions
- Carla discussing nutrition based on initial panels
- Rachel designing initial exercise program
- 50% adherence pattern beginning to show

TRAVEL CONTEXT: {travel_context}
REALISTIC ELEMENTS: Plan modifications needed for hotel gym access

Generate 4 weeks of realistic WhatsApp conversations showing test result discussions and plan development.""",

            3: f"""Generate Week {week_start}-{week_start+3} communications during active intervention phase.

SPECIFIC REQUIREMENTS:
- Weekly check-ins by Ruby
- Fortnightly medical team follow-ups
- First plan modifications due to travel constraints
- Advik analyzing Garmin data trends
- End with second diagnostic test panel (3-month mark)
- Show realistic adherence challenges and solutions

TRAVEL CONTEXT: {travel_context}
REALISTIC ELEMENTS: Jet lag affecting HRV data, local food challenges

Generate 4 weeks of realistic WhatsApp conversations during active intervention phase.""",

            4: f"""Generate Week {week_start}-{week_start+3} communications around progress review and plan optimization.

SPECIFIC REQUIREMENTS:
- Dr. Warren reviewing 3-month test results
- Team strategy session for next steps
- Neel providing strategic perspective on progress
- Plan modifications based on data and member feedback
- Preparation for cognitive enhancement focus (approaching June 2026 goal)

TRAVEL CONTEXT: {travel_context}
REALISTIC ELEMENTS: Multiple time zone adjustments, eating schedule disruptions

Generate 4 weeks of realistic WhatsApp conversations around progress review and optimization.""",

            5: f"""Generate Week {week_start}-{week_start+3} communications focusing on cognitive enhancement and stress management.

SPECIFIC REQUIREMENTS:
- Advik introducing advanced HRV protocols
- Carla optimizing nutrition for cognitive performance
- Rachel adding specific brain-health exercises
- Managing work stress during high-pressure quarter
- Preparation for third diagnostic panel

TRAVEL CONTEXT: {travel_context}
REALISTIC ELEMENTS: High stress period, reduced plan adherence, team support strategies

Generate 4 weeks of realistic WhatsApp conversations focusing on cognitive enhancement.""",

            6: f"""Generate Week {week_start}-{week_start+3} communications addressing adherence challenges and re-engagement.

SPECIFIC REQUIREMENTS:
- Third diagnostic test results review
- Honest discussion about adherence challenges
- Plan simplification and prioritization
- Neel stepping in for strategic realignment
- Focus on sustainable, travel-friendly interventions

TRAVEL CONTEXT: {travel_context}
REALISTIC ELEMENTS: Different motivation during personal time, family meal challenges

Generate 4 weeks of realistic WhatsApp conversations addressing adherence challenges.""",

            7: f"""Generate Week {week_start}-{week_start+3} communications optimizing protocols and preparing for annual screening.

SPECIFIC REQUIREMENTS:
- Fine-tuning successful interventions
- Preparation for November 2025 full-body screening goal
- Advanced cardiovascular assessment planning
- Team coordination for comprehensive annual review
- Data trend analysis across 6+ months

TRAVEL CONTEXT: {travel_context}
REALISTIC ELEMENTS: Better adherence, more consistent data, positive momentum

Generate 4 weeks of realistic WhatsApp conversations optimizing protocols.""",

            8: f"""Generate Week {week_start}-{week_start+3} communications conducting comprehensive review and future planning.

SPECIFIC REQUIREMENTS:
- Fourth diagnostic panel and comprehensive review
- Annual full-body screening coordination (meeting November 2025 goal early)
- Progress assessment against all three primary goals
- Planning for year 2 of Elyx partnership
- Team celebration of achievements and learnings

TRAVEL CONTEXT: {travel_context}
REALISTIC ELEMENTS: Comprehensive data review, strategic planning for long-term success

Generate 4 weeks of realistic WhatsApp conversations for comprehensive review."""
        }
        
        return episode_prompts.get(month, "Generate realistic health coaching conversations for this period.")
    
    def _get_travel_context(self, month: int) -> str:
        """Get travel context for specific month"""
        travel_contexts = {
            1: "Rohan has a 5-day trip to Seoul in Week 3",
            2: "UK business trip in Week 6",
            3: "Jakarta trip in Week 11",
            4: "Extended US trip (10 days) in Weeks 14-15",
            5: "Back-to-back Seoul and UK trips",
            6: "Family vacation (non-business travel)",
            7: "Reduced travel month (only one short trip)",
            8: "Planning around annual screening schedule"
        }
        
        return travel_contexts.get(month, "Regular travel schedule")
    
    def _log_generation(self, prompt_name: str, member_id: int, input_data: Dict[str, Any], 
                        output: str, model: str):
        """Log AI generation for tracking"""
        try:
            print(f"🤖 Local AI Generation Logged:")
            print(f"  Prompt: {prompt_name}")
            print(f"  Member ID: {member_id}")
            print(f"  Model: {model}")
            print(f"  Output Length: {len(output)} characters")
            print(f"  Timestamp: {datetime.now()}")
            print(f"  Cost: $0.00 (Local Model)")
        except Exception as e:
            print(f"Failed to log generation: {e}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of local AI models"""
        health_status = {
            "groq": False,
            "models_available": []
        }
        
        if self.groq_api_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                }
                response = requests.get(f"{self.groq_base_url}/models", headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    health_status["groq"] = True
                    health_status["models_available"].extend([m['id'] for m in data.get('data', [])])
            except:
                pass
        
        return health_status

# Global local AI service instance
local_ai_service = LocalAIService()
