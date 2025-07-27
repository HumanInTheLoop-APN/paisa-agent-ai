import axios from "axios";
import firebase from "firebase/compat/app";
import * as firebaseui from "firebaseui";
import {
  UserRegistrationRequest,
  UserLoginRequest,
  UserProfileUpdateRequest,
  UserConsentUpdateRequest,
  AuthResponse,
  ProfileResponse,
} from "../types/auth";

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
    const currentUser = firebase.auth().currentUser;
    if (!currentUser) {
      console.log("No Firebase user found");
      return null;
    }

    // Force token refresh to ensure we have a fresh token
    const idToken = await currentUser.getIdToken(true);
    console.log("🔄 Token refreshed successfully");
    return idToken;
  } catch (error) {
    console.error("Error refreshing token:", error);
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
    console.error("Error in request interceptor:", error);
  }

  return config;
});

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      console.log("🔄 401 error received, attempting token refresh...");

      try {
        // Try to refresh the token
        const freshToken = await getFreshToken();

        if (freshToken) {
          // Retry the original request with fresh token
          const originalRequest = error.config;
          originalRequest.headers.Authorization = `Bearer ${freshToken}`;
          localStorage.setItem("authToken", freshToken);

          console.log("🔄 Retrying request with fresh token");
          return api(originalRequest);
        } else {
          // Token refresh failed, user needs to re-authenticate
          console.log("❌ Token refresh failed, redirecting to login");
          localStorage.removeItem("authToken");
          localStorage.removeItem("user");
          window.location.href = "/login";
        }
      } catch (refreshError) {
        console.error("Error during token refresh:", refreshError);
        localStorage.removeItem("authToken");
        localStorage.removeItem("user");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export const authService = {
  // Register a new user
  async register(userData: UserRegistrationRequest): Promise<AuthResponse> {
    const response = await api.post("/auth/register", userData);
    return response.data;
  },

  // Login user with email or phone
  async login(credentials: UserLoginRequest): Promise<AuthResponse> {
    const response = await api.post("/auth/login", credentials);
    return response.data;
  },

  // Firebase authentication (handles all FirebaseUI auth methods)
  async googleSignIn(idToken: string): Promise<AuthResponse> {
    const response = await api.post("/auth/firebase-auth", {
      id_token: idToken,
    });
    return response.data;
  },

  // Get user profile
  async getProfile(): Promise<ProfileResponse> {
    const response = await api.get("/auth/profile");
    return response.data;
  },

  // Update user profile
  async updateProfile(
    profileData: UserProfileUpdateRequest
  ): Promise<{ message: string }> {
    const response = await api.put("/auth/profile", profileData);
    return response.data;
  },

  // Update user consents
  async updateConsents(
    consentData: UserConsentUpdateRequest
  ): Promise<{ message: string }> {
    const response = await api.put("/auth/consents", consentData);
    return response.data;
  },

  // Logout user with proper Firebase sign-out
  async logout(): Promise<{ message: string }> {
    try {
      // Call backend logout endpoint
      const response = await api.post("/auth/logout");

      // Sign out from Firebase Auth
      await firebase.auth().signOut();

      // Reset FirebaseUI if it exists
      const ui = firebaseui.auth.AuthUI.getInstance();
      if (ui) {
        ui.reset();
      }

      // Clear local storage
      this.removeToken();

      return response.data;
    } catch (error) {
      console.error("Logout error:", error);

      // Even if backend call fails, clean up locally
      try {
        await firebase.auth().signOut();
        const ui = firebaseui.auth.AuthUI.getInstance();
        if (ui) {
          ui.reset();
        }
      } catch (firebaseError) {
        console.error("Firebase sign-out error:", firebaseError);
      }

      this.removeToken();

      return { message: "Logged out locally" };
    }
  },

  // Store auth token
  setToken(token: string): void {
    localStorage.setItem("authToken", token);
  },

  // Get auth token
  getToken(): string | null {
    return localStorage.getItem("authToken");
  },

  // Remove auth token and user data
  removeToken(): void {
    localStorage.removeItem("authToken");
    localStorage.removeItem("user");
  },

  // Check if user is authenticated
  async isAuthenticated(): Promise<boolean> {
    try {
      const currentUser = firebase.auth().currentUser;
      if (!currentUser) return false;

      // Check if we can get a fresh token
      const freshToken = await getFreshToken();
      return !!freshToken;
    } catch (error) {
      console.error("Error checking authentication:", error);
      return false;
    }
  },

  // Listen to Firebase Auth state changes
  onAuthStateChanged(
    callback: (user: firebase.User | null) => void
  ): () => void {
    return firebase.auth().onAuthStateChanged(callback);
  },

  // Get current Firebase user
  getCurrentUser(): firebase.User | null {
    return firebase.auth().currentUser;
  },

  // Check if user is signed in with Firebase
  isFirebaseSignedIn(): boolean {
    return !!firebase.auth().currentUser;
  },

  // Wait for Firebase Auth to be ready and check authentication
  async waitForAuthReady(): Promise<boolean> {
    return new Promise((resolve) => {
      const unsubscribe = firebase.auth().onAuthStateChanged(async (user) => {
        unsubscribe();
        if (user) {
          const hasValidToken = await this.isAuthenticated();
          resolve(hasValidToken);
        } else {
          resolve(false);
        }
      });
    });
  },

  // Validate identifier format (email or phone)
  validateIdentifier(identifier: string): {
    isValid: boolean;
    type: "email" | "phone" | "invalid";
  } {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^[+]?[1-9][\d]{0,15}$/;

    if (emailRegex.test(identifier)) {
      return { isValid: true, type: "email" };
    } else if (phoneRegex.test(identifier.replace(/\D/g, ""))) {
      return { isValid: true, type: "phone" };
    } else {
      return { isValid: false, type: "invalid" };
    }
  },

  // Force token refresh (can be called manually if needed)
  async refreshToken(): Promise<string | null> {
    return await getFreshToken();
  },
};
