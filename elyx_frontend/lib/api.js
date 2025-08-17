import axios from "axios";

const base = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8080";

console.log("API Base URL:", base);

export const API = axios.create({
  baseURL: base,
  
});

// Add request interceptor for logging
API.interceptors.request.use(
  (config) => {
    console.log("API Request:", config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error("API Request Error:", error);
    return Promise.reject(error);
  }
);

// Add response interceptor for logging
API.interceptors.response.use(
  (response) => {
    console.log("API Response:", response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error("API Response Error:", error.response?.status, error.response?.data, error.config?.url);
    return Promise.reject(error);
  }
);

// Generate complete journey
export async function generateJourney() {
  try {
    console.log("Calling generate journey API");
    const response = await API.post("/generate-complete-journey");
    console.log("Generate journey API response:", response.data);
    return response;
  } catch (error) {
    console.error("Generate journey API error:", error);
    throw error;
  }
}

// Fetch journey timeline
export async function fetchJourneyTimeline(memberId = 1) {
  try {
    console.log("Calling fetch journey timeline API");
    const response = await API.get(`/journey/journey/timeline/${memberId}`);
    console.log("Fetch journey timeline API response:", response.data);
    return response;
  } catch (error) {
    console.error("Fetch journey timeline API error:", error);
    throw error;
  }
}

// Fetch team metrics
export async function fetchTeamMetrics(memberId = 1) {
  try {
    console.log("Calling fetch team metrics API");
    const response = await API.get(`/journey/journey/team-metrics/${memberId}`);
    console.log("Fetch team metrics API response:", response.data);
    return response;
  } catch (error) {
    console.error("Fetch team metrics API error:", error);
    throw error;
  }
}

// Fetch conversations
export async function fetchConversations(memberId = 1, month = null, week = null) {
  try {
    console.log("Calling fetch conversations API");
    let url = `/journey/journey/conversations/${memberId}`;
    const params = new URLSearchParams();
    if (month) params.append('month', month);
    if (week) params.append('week', week);
    if (params.toString()) url += `?${params.toString()}`;
    
    const response = await API.get(url);
    console.log("Fetch conversations API response:", response.data);
    return response;
  } catch (error) {
    console.error("Fetch conversations API error:", error);
    throw error;
  }
}

// Fetch decisions
export async function fetchDecisions(memberId = 1, month = null, decisionType = null) {
  try {
    console.log("Calling fetch decisions API");
    let url = `/journey/journey/decisions/${memberId}`;
    const params = new URLSearchParams();
    if (month) params.append('month', month);
    if (decisionType) params.append('decision_type', decisionType);
    if (params.toString()) url += `?${params.toString()}`;
    
    const response = await API.get(url);
    console.log("Fetch decisions API response:", response.data);
    return response;
  } catch (error) {
    console.error("Fetch decisions API error:", error);
    throw error;
  }
}

// Fetch decision context
export async function fetchDecisionContext(decisionId) {
  try {
    console.log("Calling fetch decision context API");
    const response = await API.get(`/journey/journey/decision-context/${decisionId}`);
    console.log("Fetch decision context API response:", response.data);
    return response;
  } catch (error) {
    console.error("Fetch decision context API error:", error);
    throw error;
  }
}

// Health check
export async function healthCheck() {
  try {
    console.log("Calling health check API");
    const response = await API.get("/ai/health");
    console.log("Health check API response:", response.data);
    return response;
  } catch (error) {
    console.error("Health check API error:", error);
    throw error;
  }
}

// Get available AI models
export async function getAIModels() {
  try {
    console.log("Calling get AI models API");
    const response = await API.get("/ai/models");
    console.log("Get AI models API response:", response.data);
    return response;
  } catch (error) {
    console.error("Get AI models API error:", error);
    throw error;
  }
}
