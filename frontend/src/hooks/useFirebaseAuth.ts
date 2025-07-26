import { useEffect, useState } from "react";
import { authService } from "../services/authService";
import firebase from "firebase/compat/app";
import * as firebaseui from "firebaseui";

interface UseFirebaseAuthOptions {
  containerId: string;
  onSuccess: () => void;
  onShowTOS: () => void;
  onShowPrivacy: () => void;
}

interface UseFirebaseAuthReturn {
  isLoading: boolean;
  error: string | null;
  setError: (error: string | null) => void;
}

export const useFirebaseAuth = ({
  containerId,
  onSuccess,
  onShowTOS,
  onShowPrivacy,
}: UseFirebaseAuthOptions): UseFirebaseAuthReturn => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log(`FirebaseAuth hook initialized for ${containerId}`);

    // Get existing instance or create new one
    let ui = firebaseui.auth.AuthUI.getInstance();
    if (!ui) {
      ui = new firebaseui.auth.AuthUI(firebase.auth());
    }

    const handleAuthSuccess = async (authResult: any) => {
      try {
        // Force token refresh to ensure we have a fresh token
        await authResult.user.getIdToken(true);
        const idToken = await authResult.user.getIdToken();
        console.log("🔑 Got ID token:", idToken.substring(0, 50) + "...");
        console.log("📏 Token length:", idToken.length);
        console.log("🔍 Token format check:", idToken.startsWith("eyJ"));

        const response = await authService.googleSignIn(idToken);
        console.log("🎯 Backend response:", response);

        if (response.custom_token) {
          console.log(
            "💾 Custom token received:",
            response.custom_token.substring(0, 50) + "..."
          );
          console.log("💾 Storing ID token for API calls");
          authService.setToken(idToken); // Use ID token, not custom token

          const userData = {
            id: response.user_id,
            email: response.email,
            phone: response.phone,
          };
          console.log("👤 Storing user data:", userData);
          localStorage.setItem("user", JSON.stringify(userData));

          const storedToken = authService.getToken();
          console.log("✅ Token stored successfully:", !!storedToken);

          onSuccess();
        } else {
          console.error("❌ No custom token in response");
          setError("Authentication failed. Please try again.");
        }
      } catch (error) {
        console.error("FirebaseUI sign-in error:", error);
        setError("Authentication failed. Please try again.");
      }
    };

    const getUIConfig = (): firebaseui.auth.Config => ({
      signInFlow: "popup", // Use popup to avoid redirect issues
      // Set a dummy URL since we handle success via callback
      signInSuccessUrl: window.location.origin,
      callbacks: {
        signInSuccessWithAuthResult: (authResult, redirectUrl) => {
          console.log(
            "FirebaseUI sign-in success callback triggered",
            authResult
          );

          // Handle the auth result asynchronously
          handleAuthSuccess(authResult);

          // Return false to prevent automatic redirect
          return false;
        },
        signInFailure: (error) => {
          console.error("FirebaseUI sign-in failure:", error);

          // Handle specific error types
          if (error.code === "firebaseui/anonymous-upgrade-merge-conflict") {
            setError(
              "Account merge conflict. Please try signing in with your original provider."
            );
          } else {
            setError("Authentication failed. Please try again.");
          }

          return Promise.resolve();
        },
        uiShown: () => {
          console.log("FirebaseUI UI shown");
          setIsLoading(false);
        },
      },
      signInOptions: [
        {
          provider: firebase.auth.GoogleAuthProvider.PROVIDER_ID,
          scopes: ["email", "profile"],
          customParameters: {
            // Forces account selection even when one account is available
            prompt: "select_account",
          },
          // Custom button label
          fullLabel: "Continue with Google",
        },
        {
          provider: firebase.auth.EmailAuthProvider.PROVIDER_ID,
          requireDisplayName: true,
          signInMethod:
            firebase.auth.EmailAuthProvider.EMAIL_PASSWORD_SIGN_IN_METHOD,
          fullLabel: "Continue with Email",
        },
        {
          provider: firebase.auth.PhoneAuthProvider.PROVIDER_ID,
          recaptchaParameters: {
            type: "image",
            size: "invisible",
            badge: "bottomleft",
          },
          defaultCountry: "IN", // Set default country to India
          // Custom button label
          fullLabel: "Continue with Phone",
        },
      ],
      // Use callback functions for TOS and Privacy Policy
      tosUrl: onShowTOS,
      privacyPolicyUrl: onShowPrivacy,
      // Disable account chooser
      credentialHelper: firebaseui.auth.CredentialHelper.NONE,
    });

    // Check if there's a pending redirect operation
    if (ui.isPendingRedirect()) {
      ui.start(`#${containerId}`, getUIConfig());
      return;
    }

    // Start FirebaseUI
    ui.start(`#${containerId}`, getUIConfig());

    // Cleanup function
    return () => {
      console.log(`${containerId} component cleanup`);
      // Reset UI if needed
      if (ui && !ui.isPendingRedirect()) {
        ui.reset();
      }
    };
  }, [containerId, onSuccess, onShowTOS, onShowPrivacy]);

  return {
    isLoading,
    error,
    setError,
  };
};
