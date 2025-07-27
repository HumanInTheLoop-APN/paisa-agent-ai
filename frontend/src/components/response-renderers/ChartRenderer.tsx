import React from 'react';

interface ChartData {
    type: 'chart';
    chartType?: string;
    title?: string;
    description?: string;
    datasets?: any[];
    labels?: string[];
    options?: any;
}

interface ChartRendererProps {
    data: ChartData;
}

export const ChartRenderer: React.FC<ChartRendererProps> = ({ data }) => {
    const getChartIcon = (chartType?: string) => {
        switch (chartType?.toLowerCase()) {
            case 'line':
                return '📈';
            case 'bar':
                return '📊';
            case 'pie':
                return '🥧';
            case 'doughnut':
                return '🍩';
            case 'area':
                return '📉';
            default:
                return '📊';
        }
    };

    const getChartColor = (chartType?: string) => {
        switch (chartType?.toLowerCase()) {
            case 'line':
                return 'linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)';
            case 'bar':
                return 'linear-gradient(135deg, #10B981 0%, #059669 100%)';
            case 'pie':
                return 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)';
            case 'doughnut':
                return 'linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%)';
            case 'area':
                return 'linear-gradient(135deg, #EF4444 0%, #DC2626 100%)';
            default:
                return 'linear-gradient(135deg, #6B7280 0%, #4B5563 100%)';
        }
    };

    return (
        <div style={{
            background: 'rgba(255, 255, 255, 0.95)',
            borderRadius: '16px',
            padding: '20px',
            margin: '12px 0',
            border: '1px solid rgba(0, 0, 0, 0.1)',
            boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
            textAlign: 'center'
        }}>
            <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '12px',
                marginBottom: '16px'
            }}>
                <div style={{
                    width: '50px',
                    height: '50px',
                    borderRadius: '50%',
                    background: getChartColor(data.chartType),
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontSize: '24px'
                }}>
                    {getChartIcon(data.chartType)}
                </div>
                <div>
                    <h3 style={{
                        margin: 0,
                        fontSize: '18px',
                        fontWeight: '600',
                        color: '#2d3748'
                    }}>
                        {data.title || 'Financial Chart'}
                    </h3>
                    {data.chartType && (
                        <div style={{
                            background: 'rgba(102, 126, 234, 0.1)',
                            color: '#667eea',
                            padding: '4px 12px',
                            borderRadius: '20px',
                            fontSize: '12px',
                            fontWeight: '500',
                            display: 'inline-block',
                            marginTop: '4px'
                        }}>
                            {data.chartType} Chart
                        </div>
                    )}
                </div>
            </div>

            <p style={{
                margin: '0 0 16px 0',
                color: '#6B7280',
                fontSize: '14px',
                lineHeight: '1.5'
            }}>
                {data.description || 'Chart visualization will be available soon'}
            </p>

            {/* Placeholder for future chart implementation */}
            <div style={{
                height: '200px',
                background: 'linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%)',
                borderRadius: '12px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                border: '2px dashed #D1D5DB',
                marginBottom: '16px'
            }}>
                <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '32px', marginBottom: '8px' }}>📊</div>
                    <div style={{ color: '#6B7280', fontSize: '14px' }}>
                        Chart coming soon
                    </div>
                </div>
            </div>

            {/* Chart metadata */}
            {data.datasets && data.labels && (
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
                    gap: '8px',
                    marginTop: '12px'
                }}>
                    <div style={{
                        padding: '8px 12px',
                        background: 'rgba(59, 130, 246, 0.1)',
                        borderRadius: '8px',
                        textAlign: 'center'
                    }}>
                        <div style={{ fontSize: '12px', color: '#374151', marginBottom: '2px' }}>Data Points</div>
                        <div style={{ fontWeight: '600', color: '#2563eb', fontSize: '14px' }}>
                            {data.labels.length}
                        </div>
                    </div>
                    <div style={{
                        padding: '8px 12px',
                        background: 'rgba(16, 185, 129, 0.1)',
                        borderRadius: '8px',
                        textAlign: 'center'
                    }}>
                        <div style={{ fontSize: '12px', color: '#374151', marginBottom: '2px' }}>Datasets</div>
                        <div style={{ fontWeight: '600', color: '#16a34a', fontSize: '14px' }}>
                            {data.datasets.length}
                        </div>
                    </div>
                </div>
            )}

            {/* Action buttons */}
            <div style={{
                display: 'flex',
                gap: '8px',
                justifyContent: 'center',
                marginTop: '16px'
            }}>
                <button style={{
                    background: 'rgba(59, 130, 246, 0.1)',
                    color: '#2563eb',
                    border: '1px solid rgba(59, 130, 246, 0.2)',
                    borderRadius: '8px',
                    padding: '8px 16px',
                    fontSize: '12px',
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
                    📊 View Data
                </button>
                <button style={{
                    background: 'rgba(16, 185, 129, 0.1)',
                    color: '#16a34a',
                    border: '1px solid rgba(16, 185, 129, 0.2)',
                    borderRadius: '8px',
                    padding: '8px 16px',
                    fontSize: '12px',
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
                    📥 Export
                </button>
            </div>
        </div>
    );
}; 