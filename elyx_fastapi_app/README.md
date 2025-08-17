# 🚀 Elyx Life – Member Journey API

## 🎯 Overview

The Elyx Life Member Journey API is a sophisticated health optimization platform that generates realistic, AI-powered conversations between members and health coaching teams. This system creates comprehensive 8-month health journeys with episode-specific communications, tracking progress, and providing personalized insights.

## ✨ Key Features

### **🤖 Advanced AI Integration**
- **100% FREE Local AI** - No API costs using Ollama and local models
- **Episode-Based Generation** - Month-specific conversation strategies
- **Character Consistency** - Maintains distinct team member personalities
- **Travel Integration** - Realistic travel context and constraints
- **Cultural Sensitivity** - Appropriate cultural and professional boundaries

### **📊 Comprehensive Journey Management**
- **8-Month Episodes** - Structured monthly progression
- **Weekly Conversations** - ~5 conversations per week average
- **Diagnostic Tracking** - Every 3 months test panels
- **Adherence Monitoring** - Realistic 50% success patterns
- **Plan Modifications** - Dynamic adjustments based on feedback

### **🏗️ Robust Architecture**
- **FastAPI Backend** - High-performance Python web framework
- **SQLite Database** - Lightweight, persistent data storage
- **SQLAlchemy ORM** - Professional database management
- **CORS Support** - Frontend integration ready
- **Health Monitoring** - System status and AI model health

## 🚀 Quick Start

### **1. Clone and Setup**
```bash
git clone <your-repo>
cd elyx_fastapi_app
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Initialize Database**
```bash
python init_database.py
```

### **4. Install Ollama (Local AI)**
```bash
# Download from https://ollama.ai/download
# Start service
ollama serve

# Download required model
ollama pull llama2
```

### **5. Test AI Generation**
```bash
python test_ai_generation.py
```

### **6. Start Server**
```bash
python -m uvicorn app.main:app --reload
```

### **7. Access API**
- **API**: http://localhost:8080
- **Documentation**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health

## 📡 API Endpoints

### **Core Endpoints**
- `POST /conversations/simulate` - Generate basic conversations
- `POST /conversations/generate-journey` - Episode-based generation
- `POST /generate-complete-journey` - Full 8-month journey
- `GET /conversations` - List all conversations
- `GET /journey/timeline` - Member journey timeline
- `GET /metrics` - Health and performance metrics
- `GET /persona` - Member profile information

### **AI Status Endpoints**
- `GET /ai/models` - Available AI models
- `GET /ai/health` - AI service health status

### **Health & Monitoring**
- `GET /health` - System health check
- `GET /` - API overview and features

## 🎬 Episode Structure

### **Month 1: Onboarding & Initial Assessment**
- Initial health concerns and Garmin data analysis
- Medical history collection and first diagnostic panel
- Team introduction and logistics coordination

### **Month 2: Test Results & Plan Development**
- Test result analysis and categorization
- Nutrition planning and exercise program design
- Lifestyle intervention commitment

### **Month 3: Implementation & First Adjustments**
- Active intervention and weekly monitoring
- First plan modifications due to travel constraints
- Second diagnostic panel preparation

### **Month 4: Progress Review & Optimization**
- 3-month progress assessment
- Strategy session and plan optimization
- Cognitive enhancement preparation

### **Month 5: Mid-Journey Intensification**
- Advanced HRV protocols and cognitive nutrition
- Brain-health exercises and stress management
- Third diagnostic panel preparation

### **Month 6: Course Correction & Re-engagement**
- Adherence challenges and honest discussion
- Plan simplification and strategic realignment
- Sustainable, travel-friendly interventions

### **Month 7: Optimization & Preparation**
- Protocol fine-tuning and success optimization
- Annual screening preparation and planning
- Cardiovascular assessment coordination

### **Month 8: Annual Review & Future Planning**
- Fourth diagnostic panel and comprehensive review
- Annual screening coordination and progress assessment
- Year 2 planning and celebration

## 🤖 AI Generation Features

### **Character Profiles**
- **Ruby (Concierge)**: Empathetic logistics coordinator
- **Dr. Warren (Medical Strategist)**: Clinical authority
- **Advik (Performance Scientist)**: Data-driven wearables expert
- **Carla (Nutritionist)**: Behavioral change specialist
- **Rachel (PT)**: Movement and form expert
- **Neel (Lead)**: Strategic relationship manager

### **Realistic Elements**
- **Time Stamps**: Business hours, time zones, travel delays
- **Friction Points**: Scheduling conflicts, communication gaps
- **Travel Integration**: Jet lag effects, local challenges
- **Adherence Patterns**: Realistic success rates and challenges

## 🔧 Configuration

### **Environment Variables**
```bash
# Database
DATABASE_URL=sqlite:///./elyx_journey.db

# Local AI
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODELS=llama2

# Application
DEBUG=True
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### **AI Model Settings**
```python
# Temperature: 0.7 (balanced creativity)
# Top-p: 0.9 (response diversity)
# Max tokens: 1000 (response length)
```

## 🧪 Testing

### **Test Scripts**
- **`test_ai_generation.py`** - Comprehensive AI testing
- **API Endpoints** - Direct endpoint testing
- **Database Verification** - Data persistence testing

### **Test Scenarios**
- ✅ Basic AI service functionality
- ✅ Episode-specific generation
- ✅ Complete journey generation
- ✅ Character consistency
- ✅ Travel context integration

## 🚨 Troubleshooting

### **Common Issues**

#### **Ollama Not Available**
```bash
# Check if Ollama is running
ollama serve

# Check port availability
netstat -an | grep 11434

# Restart Ollama
ollama stop
ollama serve
```

#### **Model Not Found**
```bash
# Download required model
ollama pull llama2

# Check available models
ollama list
```

#### **Generation Failures**
```bash
# Check AI service health
curl http://localhost:8080/ai/health

# Check model availability
curl http://localhost:8080/ai/models
```

## 📊 Data Models

### **Core Entities**
- **Member**: Profile, preferences, health goals
- **Conversation**: Messages, timestamps, tags
- **HealthEvent**: Medical events, test results
- **Decision**: Health decisions, reasoning, confidence
- **Metrics**: Performance tracking and analysis

### **AI Integration**
- **AIPrompt**: Master prompts for different scenarios
- **AIIntegration**: Model configuration and settings
- **AIGenerationLog**: Generation tracking and analytics

## 🚀 Production Deployment

### **Requirements**
- Python 3.8+
- 8GB+ RAM (for AI models)
- SQLite or PostgreSQL database
- Ollama service running

### **Performance Optimization**
```bash
# CPU optimization
export OMP_NUM_THREADS=4

# GPU acceleration (if available)
export CUDA_VISIBLE_DEVICES=0

# Memory optimization
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
```

## 📚 Documentation

### **Detailed Guides**
- **[Enhanced AI README](ENHANCED_AI_README.md)** - Comprehensive AI system documentation
- **[Local AI Setup](LOCAL_AI_SETUP.md)** - Ollama installation and configuration
- **API Documentation** - Interactive docs at `/docs` endpoint

### **Code Structure**
```
elyx_fastapi_app/
├── app/
│   ├── services/
│   │   ├── local_ai_service.py     # Enhanced AI service
│   │   ├── generator.py            # Basic conversation generation
│   │   └── journey_builder.py      # Journey construction
│   ├── models/
│   │   ├── database.py             # Database models
│   │   └── schemas.py              # API schemas
│   ├── routes/                     # API endpoints
│   ├── database.py                 # Database configuration
│   └── main.py                     # FastAPI application
├── requirements.txt                 # Python dependencies
├── setup_local_ai.bat              # Windows setup script
├── test_ai_generation.py           # AI testing script
└── README.md                       # This file
```

## 🎯 Use Cases

### **Health Coaching Platforms**
- Realistic conversation simulation
- Member journey visualization
- Progress tracking and analytics
- Team coordination training

### **Healthcare Training**
- Communication skill development
- Patient interaction simulation
- Travel and constraint management
- Cultural sensitivity training

### **Research & Development**
- AI conversation generation
- Healthcare communication patterns
- Travel impact on health plans
- Adherence pattern analysis

## 🔮 Future Roadmap

### **Phase 1 (Current)**
- ✅ Episode-based generation
- ✅ Character consistency
- ✅ Travel integration
- ✅ Basic AI models

### **Phase 2 (Next)**
- 🎯 Multi-model support
- 🎯 Advanced prompting
- 🎯 Real-time generation
- 🎯 Quality scoring

### **Phase 3 (Future)**
- 🎯 Voice generation
- 🎯 Video simulation
- 🎯 Wearable integration
- 🎯 Calendar sync

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Run tests and linting
5. Submit a pull request

### **Testing Guidelines**
- Run `python test_ai_generation.py` before committing
- Test API endpoints with different parameters
- Verify database operations and data integrity
- Check AI generation quality and consistency

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Ollama** - Local AI model inference
- **FastAPI** - High-performance web framework
- **SQLAlchemy** - Database toolkit and ORM
- **Meta** - Llama2 open-source model

---

## 🎉 Get Started Today!

Transform your health coaching platform with realistic, AI-powered conversations that maintain professional standards while providing engaging member experiences.

**🚀 Start your journey: `python -m uvicorn app.main:app --reload`**

**📚 Learn more: [Enhanced AI README](ENHANCED_AI_README.md)**

**🤖 Test AI: `python test_ai_generation.py`**
