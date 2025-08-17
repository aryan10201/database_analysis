# Environment Configuration Setup

This guide will help you create and configure the `.env` file required for the Elyx Life backend application.

## 🔧 Quick Setup

### Step 1: Create the .env file

Navigate to your backend directory and create a `.env` file:

```bash
cd elyx_frontend
touch .env.local  # On Windows: type nul > .env
```

### Step 2: Copy the configuration

Open the `.env.local` file in your text editor and paste the following configuration:

```env
NEXT_PUBLIC_API_BASE=http://localhost:8080
```