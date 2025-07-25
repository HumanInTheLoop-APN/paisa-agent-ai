import React, { useState, useEffect } from 'react';
import { authService } from '../services/authService';
import { UserProfile as UserProfileType, UserConsents } from '../types/auth';

export const UserProfile: React.FC = () => {
    const [profile, setProfile] = useState<UserProfileType | null>(null);
    const [consents, setConsents] = useState<UserConsents | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [editing, setEditing] = useState(false);
    const [saving, setSaving] = useState(false);

    const [editForm, setEditForm] = useState({
        name: '',
        country: '',
        risk_profile: '',
    });

    const [consentForm, setConsentForm] = useState({
        store_financial_snippets: false,
        store_artifacts: false,
        retention_days: 30,
    });

    useEffect(() => {
        loadProfile();
    }, []);

    const loadProfile = async () => {
        try {
            const response = await authService.getProfile();
            setProfile(response.profile);
            setConsents(response.consents);

            setEditForm({
                name: response.profile.name,
                country: response.profile.country,
                risk_profile: response.profile.risk_profile,
            });

            setConsentForm({
                store_financial_snippets: response.consents.store_financial_snippets,
                store_artifacts: response.consents.store_artifacts,
                retention_days: response.consents.retention_days,
            });
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to load profile');
        } finally {
            setLoading(false);
        }
    };

    const handleProfileSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        setError('');

        try {
            await authService.updateProfile(editForm);
            await loadProfile(); // Reload to get updated data
            setEditing(false);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to update profile');
        } finally {
            setSaving(false);
        }
    };

    const handleConsentSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        setError('');

        try {
            await authService.updateConsents(consentForm);
            await loadProfile(); // Reload to get updated data
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to update consents');
        } finally {
            setSaving(false);
        }
    };

    const handleLogout = async () => {
        try {
            await authService.logout();
            authService.removeToken();
            window.location.reload();
        } catch (err) {
            console.error('Logout error:', err);
            authService.removeToken();
            window.location.reload();
        }
    };

    if (loading) {
        return (
            <div style={{ textAlign: 'center', padding: '2rem' }}>
                <div>Loading profile...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div style={{ textAlign: 'center', padding: '2rem' }}>
                <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>
                <button onClick={loadProfile}>Retry</button>
            </div>
        );
    }

    return (
        <div style={{
            maxWidth: '600px',
            margin: '0 auto',
            padding: '2rem',
            background: 'white',
            borderRadius: '8px',
            boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
        }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h2 style={{ color: '#2962FF', margin: 0 }}>User Profile</h2>
                <button
                    onClick={handleLogout}
                    style={{
                        background: '#f44336',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        padding: '0.5rem 1rem',
                        cursor: 'pointer',
                    }}
                >
                    Logout
                </button>
            </div>

            {/* Profile Information */}
            <div style={{ marginBottom: '2rem' }}>
                <h3 style={{ marginBottom: '1rem', color: '#333' }}>Profile Information</h3>

                {!editing ? (
                    <div>
                        <div style={{ marginBottom: '0.5rem' }}>
                            <strong>Name:</strong> {profile?.name}
                        </div>
                        <div style={{ marginBottom: '0.5rem' }}>
                            <strong>Email:</strong> {profile?.email}
                        </div>
                        <div style={{ marginBottom: '0.5rem' }}>
                            <strong>Country:</strong> {profile?.country}
                        </div>
                        <div style={{ marginBottom: '1rem' }}>
                            <strong>Risk Profile:</strong> {profile?.risk_profile}
                        </div>
                        <button
                            onClick={() => setEditing(true)}
                            style={{
                                background: '#2962FF',
                                color: 'white',
                                border: 'none',
                                borderRadius: '4px',
                                padding: '0.5rem 1rem',
                                cursor: 'pointer',
                            }}
                        >
                            Edit Profile
                        </button>
                    </div>
                ) : (
                    <form onSubmit={handleProfileSubmit}>
                        <div style={{ marginBottom: '1rem' }}>
                            <label htmlFor="name" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                                Name
                            </label>
                            <input
                                type="text"
                                id="name"
                                value={editForm.name}
                                onChange={(e) => setEditForm(prev => ({ ...prev, name: e.target.value }))}
                                required
                                style={{
                                    width: '100%',
                                    padding: '0.75rem',
                                    border: '1px solid #ddd',
                                    borderRadius: '4px',
                                    fontSize: '1rem',
                                }}
                            />
                        </div>

                        <div style={{ marginBottom: '1rem' }}>
                            <label htmlFor="country" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                                Country
                            </label>
                            <select
                                id="country"
                                value={editForm.country}
                                onChange={(e) => setEditForm(prev => ({ ...prev, country: e.target.value }))}
                                style={{
                                    width: '100%',
                                    padding: '0.75rem',
                                    border: '1px solid #ddd',
                                    borderRadius: '4px',
                                    fontSize: '1rem',
                                }}
                            >
                                <option value="IN">India</option>
                                <option value="US">United States</option>
                                <option value="UK">United Kingdom</option>
                                <option value="CA">Canada</option>
                                <option value="AU">Australia</option>
                            </select>
                        </div>

                        <div style={{ marginBottom: '1rem' }}>
                            <label htmlFor="risk_profile" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                                Risk Profile
                            </label>
                            <select
                                id="risk_profile"
                                value={editForm.risk_profile}
                                onChange={(e) => setEditForm(prev => ({ ...prev, risk_profile: e.target.value }))}
                                style={{
                                    width: '100%',
                                    padding: '0.75rem',
                                    border: '1px solid #ddd',
                                    borderRadius: '4px',
                                    fontSize: '1rem',
                                }}
                            >
                                <option value="conservative">Conservative</option>
                                <option value="moderate">Moderate</option>
                                <option value="aggressive">Aggressive</option>
                            </select>
                        </div>

                        <div style={{ display: 'flex', gap: '1rem' }}>
                            <button
                                type="submit"
                                disabled={saving}
                                style={{
                                    background: saving ? '#ccc' : '#2962FF',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '4px',
                                    padding: '0.5rem 1rem',
                                    cursor: saving ? 'not-allowed' : 'pointer',
                                }}
                            >
                                {saving ? 'Saving...' : 'Save'}
                            </button>
                            <button
                                type="button"
                                onClick={() => setEditing(false)}
                                style={{
                                    background: '#666',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '4px',
                                    padding: '0.5rem 1rem',
                                    cursor: 'pointer',
                                }}
                            >
                                Cancel
                            </button>
                        </div>
                    </form>
                )}
            </div>

            {/* Consent Settings */}
            <div>
                <h3 style={{ marginBottom: '1rem', color: '#333' }}>Privacy & Consent Settings</h3>
                <form onSubmit={handleConsentSubmit}>
                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                            <input
                                type="checkbox"
                                checked={consentForm.store_financial_snippets}
                                onChange={(e) => setConsentForm(prev => ({ ...prev, store_financial_snippets: e.target.checked }))}
                                style={{ marginRight: '0.5rem' }}
                            />
                            Store financial conversation snippets for analysis
                        </label>
                    </div>

                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                            <input
                                type="checkbox"
                                checked={consentForm.store_artifacts}
                                onChange={(e) => setConsentForm(prev => ({ ...prev, store_artifacts: e.target.checked }))}
                                style={{ marginRight: '0.5rem' }}
                            />
                            Store generated artifacts and reports
                        </label>
                    </div>

                    <div style={{ marginBottom: '1rem' }}>
                        <label htmlFor="retention_days" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '500' }}>
                            Data Retention Period (days)
                        </label>
                        <input
                            type="number"
                            id="retention_days"
                            value={consentForm.retention_days}
                            onChange={(e) => setConsentForm(prev => ({ ...prev, retention_days: parseInt(e.target.value) || 30 }))}
                            min="1"
                            max="365"
                            style={{
                                width: '100%',
                                padding: '0.75rem',
                                border: '1px solid #ddd',
                                borderRadius: '4px',
                                fontSize: '1rem',
                            }}
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={saving}
                        style={{
                            background: saving ? '#ccc' : '#4CAF50',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            padding: '0.5rem 1rem',
                            cursor: saving ? 'not-allowed' : 'pointer',
                        }}
                    >
                        {saving ? 'Saving...' : 'Update Consent Settings'}
                    </button>
                </form>
            </div>
        </div>
    );
}; 