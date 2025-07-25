import React, { useState } from 'react';
import { useFirebaseAuth } from '../../hooks/useFirebaseAuth';
import { TermsOfServiceModal, PrivacyPolicyModal } from '../modals/AuthModals';
import 'firebaseui/dist/firebaseui.css';

interface AuthFormProps {
    title: string;
    containerId: string;
    onSuccess: () => void;
    switchText: string;
    onSwitch: () => void;
}

export const AuthForm: React.FC<AuthFormProps> = ({
    title,
    containerId,
    onSuccess,
    switchText,
    onSwitch
}) => {
    const [showTOS, setShowTOS] = useState(false);
    const [showPrivacy, setShowPrivacy] = useState(false);

    const { isLoading, error, setError } = useFirebaseAuth({
        containerId,
        onSuccess,
        onShowTOS: () => setShowTOS(true),
        onShowPrivacy: () => setShowPrivacy(true)
    });

    return (
        <>
            <div style={{
                maxWidth: '400px',
                margin: '0 auto',
                padding: '2rem',
                backgroundColor: 'white',
                borderRadius: '8px',
                boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)'
            }}>
                <h2 style={{ textAlign: 'center', marginBottom: '1.5rem', color: '#2962FF' }}>
                    {title}
                </h2>

                {/* FirebaseUI Container */}
                <div
                    id={containerId}
                    style={{
                        marginBottom: '1rem',
                        minHeight: '200px',
                        border: '1px solid #ddd',
                        borderRadius: '4px',
                        padding: '10px'
                    }}
                >
                    {isLoading && (
                        <p style={{ textAlign: 'center', color: '#666' }}>
                            Loading authentication options...
                        </p>
                    )}
                </div>

                {error && (
                    <div style={{ textAlign: 'center', color: '#d32f2f', marginBottom: '1rem' }}>
                        <p>{error}</p>
                        <button
                            onClick={() => {
                                setError(null);
                                window.location.reload();
                            }}
                            style={{
                                background: '#2962FF',
                                color: 'white',
                                border: 'none',
                                padding: '8px 16px',
                                borderRadius: '4px',
                                cursor: 'pointer'
                            }}
                        >
                            Retry
                        </button>
                    </div>
                )}

                <div style={{ textAlign: 'center' }}>
                    <p style={{ fontSize: '0.875rem', color: '#666' }}>
                        {switchText}{' '}
                        <button
                            onClick={onSwitch}
                            style={{
                                background: 'none',
                                border: 'none',
                                color: '#2962FF',
                                cursor: 'pointer',
                                textDecoration: 'underline',
                                fontSize: '0.875rem'
                            }}
                        >
                            {title === 'Login' ? 'Register' : 'Login'}
                        </button>
                    </p>
                </div>
            </div>

            <TermsOfServiceModal isOpen={showTOS} onClose={() => setShowTOS(false)} />
            <PrivacyPolicyModal isOpen={showPrivacy} onClose={() => setShowPrivacy(false)} />
        </>
    );
}; 