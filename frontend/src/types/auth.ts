export interface UserRegistrationRequest {
  email: string;
  password: string;
  name: string;
  country?: string;
  risk_profile?: string;
}

export interface UserLoginRequest {
  identifier: string; // Can be email or phone number
  password: string;
}

export interface GoogleSignInRequest {
  id_token: string;
}

export interface UserProfileUpdateRequest {
  name?: string;
  country?: string;
  risk_profile?: string;
}

export interface UserConsentUpdateRequest {
  store_financial_snippets?: boolean;
  store_artifacts?: boolean;
  retention_days?: number;
}

export interface UserProfile {
  name: string;
  email: string;
  country: string;
  risk_profile: string;
}

export interface UserConsents {
  store_financial_snippets: boolean;
  store_artifacts: boolean;
  retention_days: number;
}

export interface User {
  uid: string;
  profile: UserProfile;
  consents: UserConsents;
}

export interface AuthResponse {
  message: string;
  user_id: string;
  custom_token?: string;
  email?: string;
  phone?: string;
  is_new_user?: boolean;
}

export interface ProfileResponse {
  user_id: string;
  profile: UserProfile;
  consents: UserConsents;
}

export interface GoogleUser {
  uid: string;
  email: string;
  displayName: string;
  photoURL?: string;
}
