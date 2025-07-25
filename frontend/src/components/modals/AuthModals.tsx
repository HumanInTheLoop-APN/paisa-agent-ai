import React from 'react';

interface AuthModalProps {
    isOpen: boolean;
    onClose: () => void;
    title: string;
    children: React.ReactNode;
}

const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose, title, children }) => {
    if (!isOpen) return null;

    return (
        <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 10000
        }}>
            <div style={{
                backgroundColor: 'white',
                padding: '2rem',
                borderRadius: '8px',
                maxWidth: '500px',
                maxHeight: '80vh',
                overflow: 'auto'
            }}>
                <h2>{title}</h2>
                {children}
                <button
                    onClick={onClose}
                    style={{
                        background: '#2962FF',
                        color: 'white',
                        border: 'none',
                        padding: '8px 16px',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        marginTop: '1rem'
                    }}
                >
                    Close
                </button>
            </div>
        </div>
    );
};

interface TermsOfServiceModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const TermsOfServiceModal: React.FC<TermsOfServiceModalProps> = ({ isOpen, onClose }) => (
    <AuthModal isOpen={isOpen} onClose={onClose} title="Terms of Service">
        <p>
            By using Talk to Your Money, you agree to these terms and conditions.
            You must be at least 18 years old to use this service. We reserve the right
            to modify these terms at any time.
        </p>
        <p>
            This application helps you manage your financial data and provides AI-powered
            insights. You retain ownership of your data, and we are committed to protecting
            your privacy and security.
        </p>
    </AuthModal>
);

interface PrivacyPolicyModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const PrivacyPolicyModal: React.FC<PrivacyPolicyModalProps> = ({ isOpen, onClose }) => (
    <AuthModal isOpen={isOpen} onClose={onClose} title="Privacy Policy">
        <p>
            We respect your privacy and are committed to protecting your personal data.
            We collect and process your financial information only to provide you with
            personalized insights and recommendations.
        </p>
        <p>
            Your data is encrypted and stored securely. We do not sell your personal
            information to third parties. You have the right to access, modify, or
            delete your data at any time.
        </p>
    </AuthModal>
); 