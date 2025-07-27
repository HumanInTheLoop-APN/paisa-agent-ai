import React from 'react';

interface InvestmentRecommendation {
    title: string;
    description: string;
    expectedReturn?: string;
    riskLevel?: 'low' | 'medium' | 'high';
    investmentAmount?: number;
    category?: string;
    pros?: string[];
    cons?: string[];
}

interface InvestmentRecommendationsData {
    recommendations: InvestmentRecommendation[];
    summary?: string;
}

interface InvestmentRecommendationsRendererProps {
    data: InvestmentRecommendationsData;
}

export const InvestmentRecommendationsRenderer: React.FC<InvestmentRecommendationsRendererProps> = ({ data }) => {
    const getRiskColor = (riskLevel?: string) => {
        switch (riskLevel?.toLowerCase()) {
            case 'low':
                return '#10B981';
            case 'medium':
                return '#F59E0B';
            case 'high':
                return '#EF4444';
            default:
                return '#6B7280';
        }
    };

    const getRiskBackground = (riskLevel?: string) => {
        switch (riskLevel?.toLowerCase()) {
            case 'low':
                return 'rgba(16, 185, 129, 0.1)';
            case 'medium':
                return 'rgba(245, 158, 11, 0.1)';
            case 'high':
                return 'rgba(239, 68, 68, 0.1)';
            default:
                return 'rgba(107, 114, 128, 0.1)';
        }
    };

    const formatCurrency = (amount?: number) => {
        if (!amount) return 'N/A';
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    };

    return (
        <div style={{
            background: 'rgba(255, 255, 255, 0.95)',
            borderRadius: '16px',
            padding: '20px',
            margin: '12px 0',
            border: '1px solid rgba(0, 0, 0, 0.1)',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)'
        }}>
            <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginBottom: '16px'
            }}>
                <div style={{
                    width: '40px',
                    height: '40px',
                    borderRadius: '50%',
                    background: 'linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '18px'
                }}>
                    💡
                </div>
                <h3 style={{
                    margin: 0,
                    fontSize: '18px',
                    fontWeight: '600',
                    color: '#2d3748'
                }}>
                    Investment Recommendations
                </h3>
            </div>

            {data.summary && (
                <p style={{
                    margin: '0 0 16px 0',
                    color: '#6B7280',
                    fontSize: '14px',
                    lineHeight: '1.5',
                    padding: '12px 16px',
                    background: 'rgba(139, 92, 246, 0.1)',
                    borderRadius: '8px',
                    border: '1px solid rgba(139, 92, 246, 0.2)'
                }}>
                    {data.summary}
                </p>
            )}

            <div style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '16px'
            }}>
                {data.recommendations.map((rec, index) => (
                    <div key={index} style={{
                        padding: '16px',
                        background: 'rgba(16, 185, 129, 0.05)',
                        borderRadius: '12px',
                        border: '1px solid rgba(16, 185, 129, 0.2)',
                        borderLeft: '4px solid #10B981'
                    }}>
                        <div style={{
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'flex-start',
                            marginBottom: '8px'
                        }}>
                            <h4 style={{
                                margin: 0,
                                fontSize: '16px',
                                fontWeight: '600',
                                color: '#2d3748'
                            }}>
                                {rec.title}
                            </h4>
                            {rec.category && (
                                <div style={{
                                    background: 'rgba(139, 92, 246, 0.1)',
                                    color: '#7C3AED',
                                    padding: '4px 8px',
                                    borderRadius: '12px',
                                    fontSize: '11px',
                                    fontWeight: '500'
                                }}>
                                    {rec.category}
                                </div>
                            )}
                        </div>

                        <p style={{
                            margin: '0 0 12px 0',
                            color: '#6B7280',
                            fontSize: '14px',
                            lineHeight: '1.5'
                        }}>
                            {rec.description}
                        </p>

                        <div style={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
                            gap: '8px',
                            marginBottom: '12px'
                        }}>
                            {rec.expectedReturn && (
                                <div style={{
                                    padding: '8px 12px',
                                    background: 'rgba(16, 185, 129, 0.1)',
                                    borderRadius: '8px',
                                    textAlign: 'center'
                                }}>
                                    <div style={{ fontSize: '11px', color: '#374151', marginBottom: '2px' }}>Expected Return</div>
                                    <div style={{ fontWeight: '600', color: '#16a34a', fontSize: '13px' }}>
                                        {rec.expectedReturn}
                                    </div>
                                </div>
                            )}

                            {rec.investmentAmount && (
                                <div style={{
                                    padding: '8px 12px',
                                    background: 'rgba(59, 130, 246, 0.1)',
                                    borderRadius: '8px',
                                    textAlign: 'center'
                                }}>
                                    <div style={{ fontSize: '11px', color: '#374151', marginBottom: '2px' }}>Min Investment</div>
                                    <div style={{ fontWeight: '600', color: '#2563eb', fontSize: '13px' }}>
                                        {formatCurrency(rec.investmentAmount)}
                                    </div>
                                </div>
                            )}

                            {rec.riskLevel && (
                                <div style={{
                                    padding: '8px 12px',
                                    background: getRiskBackground(rec.riskLevel),
                                    borderRadius: '8px',
                                    textAlign: 'center'
                                }}>
                                    <div style={{ fontSize: '11px', color: '#374151', marginBottom: '2px' }}>Risk Level</div>
                                    <div style={{
                                        fontWeight: '600',
                                        color: getRiskColor(rec.riskLevel),
                                        fontSize: '13px',
                                        textTransform: 'capitalize'
                                    }}>
                                        {rec.riskLevel}
                                    </div>
                                </div>
                            )}
                        </div>

                        {(rec.pros || rec.cons) && (
                            <div style={{
                                display: 'grid',
                                gridTemplateColumns: rec.pros && rec.cons ? '1fr 1fr' : '1fr',
                                gap: '12px'
                            }}>
                                {rec.pros && rec.pros.length > 0 && (
                                    <div>
                                        <div style={{
                                            fontSize: '12px',
                                            fontWeight: '600',
                                            color: '#16a34a',
                                            marginBottom: '6px'
                                        }}>
                                            ✅ Pros
                                        </div>
                                        <ul style={{
                                            margin: 0,
                                            paddingLeft: '16px',
                                            fontSize: '12px',
                                            color: '#6B7280'
                                        }}>
                                            {rec.pros.map((pro, idx) => (
                                                <li key={idx}>{pro}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                {rec.cons && rec.cons.length > 0 && (
                                    <div>
                                        <div style={{
                                            fontSize: '12px',
                                            fontWeight: '600',
                                            color: '#dc2626',
                                            marginBottom: '6px'
                                        }}>
                                            ❌ Cons
                                        </div>
                                        <ul style={{
                                            margin: 0,
                                            paddingLeft: '16px',
                                            fontSize: '12px',
                                            color: '#6B7280'
                                        }}>
                                            {rec.cons.map((con, idx) => (
                                                <li key={idx}>{con}</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        )}

                        <div style={{
                            display: 'flex',
                            gap: '8px',
                            marginTop: '12px'
                        }}>
                            <button style={{
                                background: 'rgba(16, 185, 129, 0.1)',
                                color: '#16a34a',
                                border: '1px solid rgba(16, 185, 129, 0.2)',
                                borderRadius: '6px',
                                padding: '6px 12px',
                                fontSize: '11px',
                                fontWeight: '500',
                                cursor: 'pointer',
                                transition: 'all 0.2s ease'
                            }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.background = 'rgba(16, 185, 129, 0.2)';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.background = 'rgba(16, 185, 129, 0.1)';
                                }}>
                                📈 Learn More
                            </button>
                            <button style={{
                                background: 'rgba(59, 130, 246, 0.1)',
                                color: '#2563eb',
                                border: '1px solid rgba(59, 130, 246, 0.2)',
                                borderRadius: '6px',
                                padding: '6px 12px',
                                fontSize: '11px',
                                fontWeight: '500',
                                cursor: 'pointer',
                                transition: 'all 0.2s ease'
                            }}
                                onMouseEnter={(e) => {
                                    e.currentTarget.style.background = 'rgba(59, 130, 246, 0.2)';
                                }}
                                onMouseLeave={(e) => {
                                    e.currentTarget.style.background = 'rgba(59, 130, 246, 0.1)';
                                }}>
                                💰 Invest Now
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}; 