# FiSight Frontend

A React-based frontend for the FiSight financial advisor application with integrated authentication using FirebaseUI.

## Features

- **Professional Authentication UI**: Pre-built, customizable authentication forms using FirebaseUI
- **Multi-Method Authentication**:
  - Email/Password login and registration
  - Google Sign-in integration
  - Phone number authentication
- **User Profile Management**: View and edit profile information
- **Privacy Settings**: Manage consent preferences and data retention
- **Chat Interface**: Financial advisor chat (basic implementation)
- **Responsive Design**: Clean, modern UI with consistent styling

## Setup

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend server running on `http://localhost:8000`
- Firebase project configured

### Installation

1. Install dependencies:

```bash
npm install
```

2. Configure environment variables:
   Create a `.env` file in the frontend directory:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000

# Firebase Configuration (required for FirebaseUI)
REACT_APP_FIREBASE_API_KEY=your-firebase-api-key
REACT_APP_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=123456789
REACT_APP_FIREBASE_APP_ID=your-app-id
```

3. Start the development server:

```bash
npm start
```

The application will open at `http://localhost:3000`

## Authentication Features

### Login Methods

1. **Email/Password Login**: Traditional email and password authentication
2. **Google Sign-in**: One-click authentication using Google account
3. **Phone Number Authentication**: SMS-based authentication with reCAPTCHA

### Registration

- **Email Registration**: Create account with email, password, and profile information
- **Google Sign-in**: Automatic account creation when using Google sign-in
- **Profile Setup**: Configure country, risk profile, and consent preferences

### Security Features

- Automatic token management
- Secure API communication
- Automatic logout on authentication errors
- Input validation and sanitization
- Professional FirebaseUI components with built-in security

## Usage

### Authentication Flow

1. **Registration**: New users can create an account with:

   - Full name
   - Email address (required for registration)
   - Password
   - Country selection
   - Risk profile preference
   - Or use Google Sign-in for instant registration

2. **Login**: Existing users can log in with:

   - Email address and password
   - Google Sign-in
   - Phone number (SMS verification)

3. **Profile Management**: Authenticated users can:
   - View their profile information
   - Edit personal details
   - Update privacy and consent settings
   - Logout

### API Integration

The frontend integrates with your FastAPI backend endpoints:

- `POST /auth/register` - User registration
- `POST /auth/login` - User login (email/phone)
- `POST /auth/google-signin` - Google sign-in
- `GET /auth/profile` - Get user profile
- `PUT /auth/profile` - Update user profile
- `PUT /auth/consents` - Update consent settings
- `POST /auth/logout` - User logout

### Environment Variables

Required environment variables:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000

# Firebase Configuration (for FirebaseUI)
REACT_APP_FIREBASE_API_KEY=your-api-key
REACT_APP_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=123456789
REACT_APP_FIREBASE_APP_ID=your-app-id
```

## Testing the Authentication

1. **Start the Backend**: Make sure your FastAPI server is running
2. **Start the Frontend**: Run `npm start`
3. **Test Email Registration**: Use the FirebaseUI registration form
4. **Test Email Login**: Use the FirebaseUI login form
5. **Test Google Sign-in**: Click the "Continue with Google" button
6. **Test Phone Authentication**: Use the phone number option
7. **Test Profile Management**: Navigate to the Profile tab
8. **Test Logout**: Use the logout button

## File Structure

```
src/
├── components/
│   ├── Login.tsx          # Login component with FirebaseUI
│   ├── Register.tsx       # Registration component with FirebaseUI
│   ├── UserProfile.tsx    # Profile management component
│   └── Chat.tsx          # Chat interface component
├── services/
│   └── authService.ts     # Authentication API service
├── types/
│   └── auth.ts           # TypeScript type definitions
├── config/
│   ├── firebase.ts       # Firebase configuration
│   └── firebaseui.ts     # FirebaseUI configuration
└── App.tsx               # Main application component
```

## Firebase Setup

To enable FirebaseUI authentication:

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Authentication and configure providers:
   - Email/Password
   - Google Sign-in
   - Phone Number (optional)
3. Get your Firebase configuration from Project Settings
4. Add the configuration to your `.env` file
5. Configure authorized domains in Firebase Console to include `localhost:3000`

### FirebaseUI Features

- **Professional UI**: Pre-built, responsive authentication forms
- **Multiple Providers**: Email, Google, Phone, and more
- **Customizable**: Theme, branding, and behavior options
- **Accessibility**: Built-in ARIA support and keyboard navigation
- **Error Handling**: Automatic error display and recovery
- **Internationalization**: Multi-language support

## Troubleshooting

### CORS Issues

If you encounter CORS errors, ensure your backend has CORS middleware configured to allow requests from `http://localhost:3000`.

### Authentication Errors

- Verify your Firebase configuration is correct
- Check that the backend server is running
- Ensure the API endpoints are accessible
- Verify authentication providers are enabled in Firebase Console

### FirebaseUI Issues

- Check Firebase configuration in `.env` file
- Ensure authentication providers are enabled in Firebase Console
- Verify authorized domains include `localhost:3000`
- Check browser console for any JavaScript errors
- Make sure FirebaseUI package is installed: `npm install firebaseui`

### Build Issues

- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check for TypeScript errors: `npm run build`
- Verify all environment variables are set correctly

## Security Notes

- Firebase configuration is loaded at build time for optimal performance
- Authentication tokens are stored securely in localStorage
- API requests include automatic token management
- FirebaseUI provides built-in security features and validation
- All authentication flows are handled by Firebase's secure infrastructure
