import React from 'react';
import { authService } from '../services/authService';

interface SidebarProps {
    isOpen: boolean;
    onClose: () => void;
    currentPage: string;
    onPageChange: (page: string) => void;
    onToggleSidebar: () => void;
}

interface NavigationItem {
    id: string;
    label: string;
    icon: string;
    active?: boolean;
    badge?: string;
    badgeType?: string;
}

interface NavigationSection {
    section: string;
    items: NavigationItem[];
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose, currentPage, onPageChange, onToggleSidebar }) => {
    const navigationItems: NavigationSection[] = [
        {
            section: 'Dashboard',
            items: [
                { id: 'dashboard', label: 'Net Worth Overview', icon: '📊', active: true },
                { id: 'portfolio', label: 'Investment Portfolio', icon: '📈' },
                { id: 'transactions', label: 'Transactions', icon: '💰' }
            ]
        },
        {
            section: 'AI Tools',
            items: [
                { id: 'goal-planner', label: 'Financial Goal Planner', icon: '📅', badge: 'AI', badgeType: 'new' },
                { id: 'reports', label: 'Scheduled Reports', icon: '📄', badge: 'AI', badgeType: 'new' },
                { id: 'advisor', label: 'Investment Advisor', icon: '✅', badge: 'BETA', badgeType: 'beta' },
                { id: 'tax-optimizer', label: 'Tax Optimizer', icon: '📋', badge: 'BETA', badgeType: 'beta' }
            ]
        },
        {
            section: 'Account',
            items: [
                { id: 'profile', label: 'Profile Settings', icon: '👤' },
                { id: 'security', label: 'Security & Privacy', icon: '🛡️' },
                { id: 'support', label: 'Support & Help', icon: '📧' },
                { id: 'signout', label: 'Sign Out', icon: '🚪' }
            ]
        }
    ];

    const handleItemClick = (itemId: string) => {
        onToggleSidebar();
        onPageChange(itemId);
        if (window.innerWidth <= 768) {
            onClose();
        }
    };

    const getBadgeColor = (badgeType: string) => {
        switch (badgeType) {
            case 'new': return '#10B981';
            case 'beta': return '#F59E0B';
            default: return '#667eea';
        }
    };

    return (
        <>
            {/* Overlay */}
            {isOpen && (
                <div
                    style={{
                        position: 'fixed',
                        top: 0,
                        left: 0,
                        width: '100%',
                        height: '100%',
                        background: 'rgba(0, 0, 0, 0.5)',
                        zIndex: 1001,
                        opacity: isOpen ? 1 : 0,
                        visibility: isOpen ? 'visible' : 'hidden',
                        transition: 'all 0.3s ease'
                    }}
                    onClick={onClose}
                />
            )}

            {/* Sidebar */}
            <nav
                style={{
                    position: 'fixed',
                    top: 0,
                    left: isOpen ? 0 : '-300px',
                    width: window.innerWidth <= 480 ? '100%' : '300px',
                    height: '100vh',
                    background: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(20px)',
                    boxShadow: '2px 0 20px rgba(0, 0, 0, 0.1)',
                    zIndex: 1002,
                    transition: 'left 0.3s ease',
                    overflowY: 'auto'
                }}
            >
                {/* Sidebar Header */}
                <div
                    style={{
                        padding: '25px 20px',
                        borderBottom: '1px solid rgba(0, 0, 0, 0.1)',
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        color: 'white',
                        position: 'relative'
                    }}
                >
                    <button
                        onClick={onClose}
                        style={{
                            position: 'absolute',
                            top: '15px',
                            right: '15px',
                            background: 'none',
                            border: 'none',
                            color: 'white',
                            cursor: 'pointer',
                            padding: '5px',
                            borderRadius: '50%',
                            width: '35px',
                            height: '35px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            transition: 'background 0.2s ease'
                        }}
                        onMouseOver={(e) => e.currentTarget.style.background = 'rgba(255, 255, 255, 0.2)'}
                        onMouseOut={(e) => e.currentTarget.style.background = 'none'}
                    >
                        ✕
                    </button>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '15px' }}>
                        <div
                            style={{
                                width: '50px',
                                height: '50px',
                                borderRadius: '50%',
                                background: 'rgba(255, 255, 255, 0.2)',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                fontSize: '20px',
                                fontWeight: 'bold'
                            }}
                        >
                            RS
                        </div>
                        <div>
                            <h3 style={{ margin: 0, fontSize: '1.2rem', fontWeight: '600' }}>
                                Rajesh Sharma
                            </h3>
                            <p style={{ margin: '5px 0 0 0', fontSize: '0.9rem', opacity: 0.9 }}>
                                Premium Member
                            </p>
                        </div>
                    </div>
                </div>

                {/* Navigation */}
                <div style={{ padding: '20px 0' }}>
                    {navigationItems.map((section, sectionIndex) => (
                        <div key={sectionIndex} style={{ marginBottom: '30px' }}>
                            <div
                                style={{
                                    padding: '0 20px 10px',
                                    fontSize: '0.8rem',
                                    fontWeight: '600',
                                    color: '#718096',
                                    textTransform: 'uppercase',
                                    letterSpacing: '1px'
                                }}
                            >
                                {section.section}
                            </div>

                            {section.items.map((item, itemIndex) => (
                                <button
                                    key={itemIndex}
                                    onClick={() => handleItemClick(item.id)}
                                    style={{
                                        width: '100%',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '15px',
                                        padding: '12px 20px',
                                        color: currentPage === item.id ? '#667eea' : '#4a5568',
                                        background: 'none',
                                        border: 'none',
                                        borderLeft: currentPage === item.id ? '3px solid #667eea' : '3px solid transparent',
                                        backgroundColor: currentPage === item.id ? 'rgba(102, 126, 234, 0.15)' : 'transparent',
                                        fontWeight: currentPage === item.id ? '600' : 'normal',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s ease',
                                        textAlign: 'left'
                                    }}
                                    onMouseOver={(e) => {
                                        if (currentPage !== item.id) {
                                            e.currentTarget.style.backgroundColor = 'rgba(102, 126, 234, 0.1)';
                                            e.currentTarget.style.borderLeftColor = '#667eea';
                                            e.currentTarget.style.color = '#2d3748';
                                        }
                                    }}
                                    onMouseOut={(e) => {
                                        if (currentPage !== item.id) {
                                            e.currentTarget.style.backgroundColor = 'transparent';
                                            e.currentTarget.style.borderLeftColor = 'transparent';
                                            e.currentTarget.style.color = '#4a5568';
                                        }
                                    }}
                                >
                                    <span style={{ fontSize: '20px' }}>{item.icon}</span>
                                    <span style={{ flex: 1 }}>{item.label}</span>
                                    {item.badge && (
                                        <span
                                            style={{
                                                background: getBadgeColor(item.badgeType || ''),
                                                color: 'white',
                                                fontSize: '0.7rem',
                                                padding: '2px 8px',
                                                borderRadius: '12px',
                                                fontWeight: '600'
                                            }}
                                        >
                                            {item.badge}
                                        </span>
                                    )}
                                </button>
                            ))}
                        </div>
                    ))}
                </div>
            </nav>
        </>
    );
}; 