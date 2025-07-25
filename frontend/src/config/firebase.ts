// Firebase configuration for FirebaseUI (using v8 compatibility)
import "firebase/compat/auth"; // Required for FirebaseUI compatibility
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Also initialize Firebase compat for FirebaseUI
import firebase from "firebase/compat/app";
import "firebase/compat/auth";

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.REACT_APP_FIREBASE_APP_ID,
  measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID,
};

console.log("Firebase config:", firebaseConfig);

// Initialize Firebase app
const app = initializeApp(firebaseConfig);

// Get auth instance using v9 SDK (for our app logic)
export const auth = getAuth(app);

// Initialize Firebase compat if not already initialized
if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

// Export both for different use cases
export const firebaseCompat = firebase;
export { firebase }; // For FirebaseUI

console.log("Firebase app initialized:", app);
console.log("Firebase auth initialized:", auth);
console.log("Firebase compat initialized:", firebase);

export default app;
