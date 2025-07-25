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

// Add request interceptor to include auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("authToken");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("authToken");
      localStorage.removeItem("user");
      window.location.href = "/login";
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
  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) return false;

    // Check if Firebase Auth is initialized and user exists
    const firebaseUser = this.getCurrentUser();
    if (!firebaseUser) return false;

    // TODO: Optionally verify token expiry
    return true;
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
      const unsubscribe = firebase.auth().onAuthStateChanged((user) => {
        unsubscribe();
        const hasToken = this.getToken();
        resolve(!!user && !!hasToken);
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
};
