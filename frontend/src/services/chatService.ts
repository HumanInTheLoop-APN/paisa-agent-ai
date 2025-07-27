import axios from "axios";
import { authService } from "./authService";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Function to get a fresh Firebase ID token
const getFreshToken = async (): Promise<string | null> => {
  try {
    const currentUser = authService.getCurrentUser();
    if (!currentUser) {
      console.log("No Firebase user found");
      return null;
    }

    // Force token refresh to ensure we have a fresh token
    const idToken = await currentUser.getIdToken(true);
    console.log("🔄 Chat service: Token refreshed successfully");
    return idToken;
  } catch (error) {
    console.error("Error refreshing token in chat service:", error);
    return null;
  }
};

// Add request interceptor to include auth token and handle token refresh
api.interceptors.request.use(async (config) => {
  try {
    // Always get a fresh token for API calls to ensure it's not expired
    const freshToken = await getFreshToken();

    if (freshToken) {
      config.headers.Authorization = `Bearer ${freshToken}`;
      // Update stored token
      localStorage.setItem("authToken", freshToken);
    } else {
      // If no fresh token, try to use stored token as fallback
      const storedToken = localStorage.getItem("authToken");
      if (storedToken) {
        config.headers.Authorization = `Bearer ${storedToken}`;
      }
    }
  } catch (error) {
    console.error("Error in chat service request interceptor:", error);
  }

  return config;
});

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      console.log(
        "🔄 Chat service: 401 error received, attempting token refresh..."
      );

      try {
        // Try to refresh the token
        const freshToken = await getFreshToken();

        if (freshToken) {
          // Retry the original request with fresh token
          const originalRequest = error.config;
          originalRequest.headers.Authorization = `Bearer ${freshToken}`;
          localStorage.setItem("authToken", freshToken);

          console.log("🔄 Chat service: Retrying request with fresh token");
          return api(originalRequest);
        } else {
          // Token refresh failed, user needs to re-authenticate
          console.log(
            "❌ Chat service: Token refresh failed, redirecting to login"
          );
          localStorage.removeItem("authToken");
          localStorage.removeItem("user");
          window.location.href = "/login";
        }
      } catch (refreshError) {
        console.error(
          "Error during token refresh in chat service:",
          refreshError
        );
        localStorage.removeItem("authToken");
        localStorage.removeItem("user");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export interface ChatSession {
  id: string;
  user_id: string;
  title?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  content: string;
  role: "user" | "assistant";
  created_at: string;
  metadata?: any;
}

export interface ChatResponse {
  response: string;
  assistant_message?: ChatMessage;
  session_id?: string;
}

class ChatService {
  async getAuthHeaders() {
    const token = await getFreshToken();
    return {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    };
  }

  async createSession(): Promise<ChatSession> {
    const response = await api.post("/sessions");
    return response.data;
  }

  async getSessions(): Promise<ChatSession[]> {
    const response = await api.get("/sessions");
    return response.data;
  }

  async getSession(sessionId: string): Promise<ChatSession> {
    const response = await api.get(`/sessions/${sessionId}`);
    return response.data;
  }

  async sendMessage(
    sessionId: string,
    message: string,
    handleStream: (stream: any) => void
  ): Promise<void> {
    // returns a stream of events, so return a streaming response
    const response = await api.post(
      `/sessions/${sessionId}/chat`,
      {
        content: message,
        metadata: {},
      },
      {
        responseType: "stream",
      }
    );
    console.log("Response", response);
    const stream = response.data;
    console.log("Stream", stream);
    handleStream(stream);
  }

  async getSessionMessages(sessionId: string): Promise<ChatMessage[]> {
    const response = await api.get(`/sessions/${sessionId}/messages`);
    return response.data;
  }

  async updateSession(
    sessionId: string,
    updates: Partial<ChatSession>
  ): Promise<ChatSession> {
    const response = await api.put(`/sessions/${sessionId}`, updates);
    return response.data;
  }

  async deleteSession(sessionId: string): Promise<{ message: string }> {
    const response = await api.delete(`/sessions/${sessionId}`);
    return response.data;
  }

  async deactivateSession(sessionId: string): Promise<{ message: string }> {
    const response = await api.post(`/sessions/${sessionId}/deactivate`);
    return response.data;
  }

  async getSessionSummary(sessionId: string): Promise<{ summary: string }> {
    const response = await api.get(`/sessions/${sessionId}/summary`);
    return response.data;
  }

  async getAllUserMessages(): Promise<ChatMessage[]> {
    const response = await api.get("/sessions/conversation");
    return response.data;
  }
}

export const chatService = new ChatService();
