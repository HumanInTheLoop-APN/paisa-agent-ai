import React from 'react';
import { AuthForm } from './shared/AuthForm';

interface LoginProps {
    onLoginSuccess: () => void;
    onSwitchToRegister: () => void;
}

export const Login: React.FC<LoginProps> = ({ onLoginSuccess, onSwitchToRegister }) => {
    return (
        <AuthForm
            title="Login"
            containerId="firebaseui-auth-container-login"
            onSuccess={onLoginSuccess}
            switchText="Don't have an account?"
            onSwitch={onSwitchToRegister}
        />
    );
}; 