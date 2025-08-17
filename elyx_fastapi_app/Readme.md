# Environment Configuration Setup

This guide will help you create and configure the `.env` file required for the Elyx Life backend application.

## 🔧 Quick Setup

### Step 1: Create the .env file

Navigate to your backend directory and create a `.env` file:

```bash
cd elyx_fastapi_app
touch .env  # On Windows: type nul > .env
```

### Step 2: Copy the configuration

Open the `.env` file in your text editor and paste the following configuration:

```env
# Database - SQLite for development (default)
DATABASE_URL=sqlite:///./elyx_journey.db

# Application settings
HOST=0.0.0.0
PORT=8080
DEBUG=true

# CORS (for frontend communication)
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# Groq AI API Key (REQUIRED)
GROQ_API_KEY=your_groq_api_key_here

# =============================================================================
# OPTIONAL SETTINGS (Can be left as defaults)
# =============================================================================

# AI generation parameters
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=1000

# Logging
LOG_LEVEL=INFO
```

### Step 3: Configure your Groq API Key

⚠️ **IMPORTANT**: You need to replace `your_groq_api_key_here` with your actual Groq API key.

1. **Get your Groq API key:**
   - Visit [Groq Console](https://console.groq.com/)
   - Sign up or log in to your account
   - Navigate to API Keys section
   - Create a new API key or copy your existing one

2. **Update the .env file:**
   ```env
   GROQ_API_KEY=gsk_your_actual_api_key_here
   ```