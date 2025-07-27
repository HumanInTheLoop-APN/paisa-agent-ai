import React from 'react';

interface FinancialMetricsData {
    netWorth?: number;
    assets?: number;
    liabilities?: number;
    investments?: number;
    savings?: number;
    monthlyIncome?: number;
    monthlyExpenses?: number;
}

interface FinancialMetricsRendererProps {
    data: FinancialMetricsData;
}

export const FinancialMetricsRenderer: React.FC<FinancialMetricsRendererProps> = ({ data }) => {
    const formatCurrency = (amount: number) => {
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
                    background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '18px'
                }}>
                    📊
                </div>
                <h3 style={{
                    margin: 0,
                    fontSize: '18px',
                    fontWeight: '600',
                    color: '#2d3748'
                }}>
                    Financial Summary
                </h3>
            </div>

            <div style={{
                display: 'grid',
                gap: '12px'
            }}>
                {data.netWorth !== undefined && (
                    <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        padding: '12px 16px',
                        background: 'rgba(16, 185, 129, 0.1)',
                        borderRadius: '12px',
                        border: '1px solid rgba(16, 185, 129, 0.2)'
                    }}>
                        <span style={{ color: '#374151', fontWeight: '500' }}>Net Worth</span>
                        <span style={{
                            fontWeight: '700',
                            color: '#059669',
                            fontSize: '16px'
                        }}>
                            {formatCurrency(data.netWorth)}
                        </span>
                    </div>
                )}

                {data.assets !== undefined && (
                    <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        padding: '12px 16px',
                        background: 'rgba(34, 197, 94, 0.1)',
                        borderRadius: '12px',
                        border: '1px solid rgba(34, 197, 94, 0.2)'
                    }}>
                        <span style={{ color: '#374151', fontWeight: '500' }}>Total Assets</span>
                        <span style={{
                            fontWeight: '600',
                            color: '#16a34a',
                            fontSize: '15px'
                        }}>
                            {formatCurrency(data.assets)}
                        </span>
                    </div>
                )}

                {data.liabilities !== undefined && (
                    <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        padding: '12px 16px',
                        background: 'rgba(239, 68, 68, 0.1)',
                        borderRadius: '12px',
                        border: '1px solid rgba(239, 68, 68, 0.2)'
                    }}>
                        <span style={{ color: '#374151', fontWeight: '500' }}>Total Liabilities</span>
                        <span style={{
                            fontWeight: '600',
                            color: '#dc2626',
                            fontSize: '15px'
                        }}>
                            {formatCurrency(data.liabilities)}
                        </span>
                    </div>
                )}

                {data.investments !== undefined && (
                    <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        padding: '12px 16px',
                        background: 'rgba(59, 130, 246, 0.1)',
                        borderRadius: '12px',
                        border: '1px solid rgba(59, 130, 246, 0.2)'
                    }}>
                        <span style={{ color: '#374151', fontWeight: '500' }}>Investments</span>
                        <span style={{
                            fontWeight: '600',
                            color: '#2563eb',
                            fontSize: '15px'
                        }}>
                            {formatCurrency(data.investments)}
                        </span>
                    </div>
                )}

                {data.savings !== undefined && (
                    <div style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        padding: '12px 16px',
                        background: 'rgba(168, 85, 247, 0.1)',
                        borderRadius: '12px',
                        border: '1px solid rgba(168, 85, 247, 0.2)'
                    }}>
                        <span style={{ color: '#374151', fontWeight: '500' }}>Savings</span>
                        <span style={{
                            fontWeight: '600',
                            color: '#9333ea',
                            fontSize: '15px'
                        }}>
                            {formatCurrency(data.savings)}
                        </span>
                    </div>
                )}

                {data.monthlyIncome !== undefined && data.monthlyExpenses !== undefined && (
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: '1fr 1fr',
                        gap: '8px',
                        marginTop: '8px'
                    }}>
                        <div style={{
                            padding: '8px 12px',
                            background: 'rgba(34, 197, 94, 0.1)',
                            borderRadius: '8px',
                            textAlign: 'center'
                        }}>
                            <div style={{ fontSize: '12px', color: '#374151', marginBottom: '4px' }}>Monthly Income</div>
                            <div style={{ fontWeight: '600', color: '#16a34a', fontSize: '14px' }}>
                                {formatCurrency(data.monthlyIncome)}
                            </div>
                        </div>
                        <div style={{
                            padding: '8px 12px',
                            background: 'rgba(239, 68, 68, 0.1)',
                            borderRadius: '8px',
                            textAlign: 'center'
                        }}>
                            <div style={{ fontSize: '12px', color: '#374151', marginBottom: '4px' }}>Monthly Expenses</div>
                            <div style={{ fontWeight: '600', color: '#dc2626', fontSize: '14px' }}>
                                {formatCurrency(data.monthlyExpenses)}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}; 