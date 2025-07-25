import React from 'react';
import { AuthForm } from './shared/AuthForm';

interface RegisterProps {
    onRegisterSuccess: () => void;
    onSwitchToLogin: () => void;
}

export const Register: React.FC<RegisterProps> = ({ onRegisterSuccess, onSwitchToLogin }) => {
    return (
        <AuthForm
            title="Register"
            containerId="firebaseui-auth-container-register"
            onSuccess={onRegisterSuccess}
            switchText="Already have an account?"
            onSwitch={onSwitchToLogin}
        />
    );
}; 