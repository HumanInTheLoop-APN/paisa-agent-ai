import React, { useState } from 'react';

export const GoalPlanner: React.FC = () => {
    const [goals] = useState([
        {
            id: 1,
            title: 'Emergency Fund',
            targetAmount: 600000,
            currentAmount: 240000,
            targetDate: '2024-12-31',
            category: 'Safety',
            priority: 'High',
            status: 'In Progress'
        },
        {
            id: 2,
            title: 'House Down Payment',
            targetAmount: 2500000,
            currentAmount: 800000,
            targetDate: '2026-06-30',
            category: 'Housing',
            priority: 'High',
            status: 'In Progress'
        },
        {
            id: 3,
            title: 'Vacation to Europe',
            targetAmount: 350000,
            currentAmount: 125000,
            targetDate: '2024-08-15',
            category: 'Lifestyle',
            priority: 'Medium',
            status: 'In Progress'
        },
        {
            id: 4,
            title: 'Child Education Fund',
            targetAmount: 5000000,
            currentAmount: 450000,
            targetDate: '2035-06-30',
            category: 'Education',
            priority: 'High',
            status: 'In Progress'
        }
    ]);

    const formatCurrency = (amount: number) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            minimumFractionDigits: 0
        }).format(amount);
    };

    const getProgressPercentage = (current: number, target: number) => {
        return Math.min((current / target) * 100, 100);
    };

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case 'High': return '#e53e3e';
            case 'Medium': return '#f59e0b';
            case 'Low': return '#38a169';
            default: return '#4a5568';
        }
    };

    const getCategoryIcon = (category: string) => {
        switch (category) {
            case 'Safety': return '🛡️';
            case 'Housing': return '🏠';
            case 'Lifestyle': return '✈️';
            case 'Education': return '🎓';
            case 'Investment': return '📈';
            default: return '🎯';
        }
    };

    return (
        <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '20px' }}>
            {/* Header */}
            <div style={{ marginBottom: '30px' }}>
                <h1 style={{ fontSize: '2.5rem', fontWeight: '300', marginBottom: '10px', color: '#2d3748' }}>
                    Financial Goal Planner
                </h1>
                <p style={{ color: '#718096', fontSize: '1.1rem' }}>Plan and track your financial goals with AI assistance</p>
            </div>

            {/* AI Assistant Card */}
            <div style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                borderRadius: '20px',
                padding: '25px',
                marginBottom: '30px',
                color: 'white',
                boxShadow: '0 15px 35px rgba(0, 0, 0, 0.1)'
            }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                    <div style={{ fontSize: '2.5rem' }}>🤖</div>
                    <div>
                        <h3 style={{ margin: 0, fontSize: '1.3rem', fontWeight: '600' }}>AI-Powered Goal Planning</h3>
                        <p style={{ margin: '5px 0 0', opacity: 0.9 }}>
                            Get personalized recommendations for achieving your financial goals faster
                        </p>
                    </div>
                    <button style={{
                        background: 'rgba(255, 255, 255, 0.2)',
                        border: 'none',
                        borderRadius: '12px',
                        padding: '12px 20px',
                        color: 'white',
                        cursor: 'pointer',
                        fontWeight: '500',
                        marginLeft: 'auto'
                    }}>
                        Get AI Suggestions
                    </button>
                </div>
            </div>

            {/* Summary Stats */}
            <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '20px',
                marginBottom: '30px'
            }}>
                <div style={{
                    background: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(10px)',
                    borderRadius: '15px',
                    padding: '20px',
                    boxShadow: '0 10px 25px rgba(0, 0, 0, 0.08)',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '1.8rem', fontWeight: 'bold', color: '#667eea', marginBottom: '5px' }}>
                        {goals.length}
                    </div>
                    <div style={{ color: '#718096', fontSize: '0.9rem' }}>Active Goals</div>
                </div>

                <div style={{
                    background: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(10px)',
                    borderRadius: '15px',
                    padding: '20px',
                    boxShadow: '0 10px 25px rgba(0, 0, 0, 0.08)',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '1.8rem', fontWeight: 'bold', color: '#38a169', marginBottom: '5px' }}>
                        {formatCurrency(goals.reduce((sum, goal) => sum + goal.currentAmount, 0))}
                    </div>
                    <div style={{ color: '#718096', fontSize: '0.9rem' }}>Total Saved</div>
                </div>

                <div style={{
                    background: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(10px)',
                    borderRadius: '15px',
                    padding: '20px',
                    boxShadow: '0 10px 25px rgba(0, 0, 0, 0.08)',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '1.8rem', fontWeight: 'bold', color: '#f59e0b', marginBottom: '5px' }}>
                        {formatCurrency(goals.reduce((sum, goal) => sum + goal.targetAmount, 0))}
                    </div>
                    <div style={{ color: '#718096', fontSize: '0.9rem' }}>Total Target</div>
                </div>

                <div style={{
                    background: 'rgba(255, 255, 255, 0.95)',
                    backdropFilter: 'blur(10px)',
                    borderRadius: '15px',
                    padding: '20px',
                    boxShadow: '0 10px 25px rgba(0, 0, 0, 0.08)',
                    textAlign: 'center'
                }}>
                    <div style={{ fontSize: '1.8rem', fontWeight: 'bold', color: '#8b5cf6', marginBottom: '5px' }}>
                        {Math.round(goals.reduce((sum, goal) => sum + getProgressPercentage(goal.currentAmount, goal.targetAmount), 0) / goals.length)}%
                    </div>
                    <div style={{ color: '#718096', fontSize: '0.9rem' }}>Average Progress</div>
                </div>
            </div>

            {/* Goals List */}
            <div style={{
                background: 'rgba(255, 255, 255, 0.95)',
                backdropFilter: 'blur(10px)',
                borderRadius: '20px',
                padding: '25px',
                boxShadow: '0 15px 35px rgba(0, 0, 0, 0.1)'
            }}>
                <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '25px'
                }}>
                    <h2 style={{ fontSize: '1.5rem', fontWeight: '600', color: '#2d3748', margin: 0 }}>
                        Your Financial Goals
                    </h2>
                    <button style={{
                        background: '#667eea',
                        color: 'white',
                        border: 'none',
                        borderRadius: '12px',
                        padding: '12px 20px',
                        cursor: 'pointer',
                        fontWeight: '500'
                    }}>
                        + Add New Goal
                    </button>
                </div>

                <div style={{ display: 'grid', gap: '20px' }}>
                    {goals.map((goal) => {
                        const progress = getProgressPercentage(goal.currentAmount, goal.targetAmount);
                        const remaining = goal.targetAmount - goal.currentAmount;
                        const daysLeft = Math.ceil((new Date(goal.targetDate).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24));

                        return (
                            <div key={goal.id} style={{
                                border: '1px solid #e2e8f0',
                                borderRadius: '15px',
                                padding: '20px',
                                background: '#f8fafc'
                            }}>
                                <div style={{
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'flex-start',
                                    marginBottom: '15px'
                                }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                        <span style={{ fontSize: '1.5rem' }}>{getCategoryIcon(goal.category)}</span>
                                        <div>
                                            <h3 style={{ margin: 0, fontSize: '1.2rem', fontWeight: '600', color: '#2d3748' }}>
                                                {goal.title}
                                            </h3>
                                            <div style={{ display: 'flex', gap: '15px', marginTop: '5px' }}>
                                                <span style={{
                                                    background: getPriorityColor(goal.priority),
                                                    color: 'white',
                                                    fontSize: '0.7rem',
                                                    padding: '2px 8px',
                                                    borderRadius: '12px',
                                                    fontWeight: '600'
                                                }}>
                                                    {goal.priority}
                                                </span>
                                                <span style={{ fontSize: '0.9rem', color: '#718096' }}>
                                                    {goal.category}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                    <div style={{ textAlign: 'right' }}>
                                        <div style={{ fontSize: '1.1rem', fontWeight: 'bold', color: '#2d3748' }}>
                                            {formatCurrency(goal.currentAmount)} / {formatCurrency(goal.targetAmount)}
                                        </div>
                                        <div style={{ fontSize: '0.9rem', color: '#718096', marginTop: '2px' }}>
                                            {daysLeft > 0 ? `${daysLeft} days left` : 'Overdue'}
                                        </div>
                                    </div>
                                </div>

                                {/* Progress Bar */}
                                <div style={{
                                    background: '#e2e8f0',
                                    borderRadius: '10px',
                                    height: '8px',
                                    marginBottom: '15px',
                                    overflow: 'hidden'
                                }}>
                                    <div style={{
                                        background: progress >= 100 ? '#38a169' : '#667eea',
                                        width: `${progress}%`,
                                        height: '100%',
                                        borderRadius: '10px',
                                        transition: 'width 0.3s ease'
                                    }} />
                                </div>

                                <div style={{
                                    display: 'grid',
                                    gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                                    gap: '15px',
                                    fontSize: '0.9rem',
                                    color: '#4a5568'
                                }}>
                                    <div>
                                        <span style={{ color: '#718096' }}>Progress: </span>
                                        <span style={{ fontWeight: '600' }}>{progress.toFixed(1)}%</span>
                                    </div>
                                    <div>
                                        <span style={{ color: '#718096' }}>Remaining: </span>
                                        <span style={{ fontWeight: '600' }}>{formatCurrency(remaining)}</span>
                                    </div>
                                    <div>
                                        <span style={{ color: '#718096' }}>Target Date: </span>
                                        <span style={{ fontWeight: '600' }}>
                                            {new Date(goal.targetDate).toLocaleDateString('en-IN')}
                                        </span>
                                    </div>
                                    <div>
                                        <span style={{ color: '#718096' }}>Status: </span>
                                        <span style={{ fontWeight: '600', color: '#38a169' }}>{goal.status}</span>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}; 