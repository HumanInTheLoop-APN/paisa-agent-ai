import React from 'react';

export const Portfolio: React.FC = () => {
  const portfolioData = [
    {
      category: 'Mutual Funds',
      totalValue: 177605,
      holdings: [
        {
          name: 'ICICI Prudential Nifty 50 Index Fund',
          value: 177605,
          units: 665.02,
          nav: 267.69,
          returns: 167578,
          returnsPercent: 1671.17
        }
      ]
    },
    {
      category: 'Indian Stocks',
      totalValue: 200642,
      holdings: [
        {
          name: 'HDFC Bank Limited',
          value: 19500,
          quantity: 12,
          ltp: 1625,
          isin: 'INE040A01034'
        },
        {
          name: 'Reliance Industries',
          value: 85000,
          quantity: 35,
          ltp: 2428,
          isin: 'INE002A01018'
        },
        {
          name: 'Infosys Limited',
          value: 96142,
          quantity: 52,
          ltp: 1849,
          isin: 'INE009A01021'
        }
      ]
    },
    {
      category: 'REITs & InvITs',
      totalValue: 2823,
      holdings: [
        {
          name: 'Brookfield India REIT',
          value: 1673,
          units: 115,
          closingRate: 14.55
        },
        {
          name: 'PowerGrid Infrastructure InvIT',
          value: 1150,
          units: 115,
          type: 'InvIT'
        }
      ]
    },
    {
      category: 'US Securities',
      totalValue: 31086,
      holdings: [
        {
          name: 'Apple Inc.',
          value: 15500,
          quantity: 8,
          ltp: 193.75
        },
        {
          name: 'Microsoft Corporation',
          value: 15586,
          quantity: 4,
          ltp: 389.65
        }
      ]
    }
  ];

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const formatPercent = (percent: number) => {
    return `${percent > 0 ? '+' : ''}${percent.toFixed(2)}%`;
  };

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '20px' }}>
      {/* Header */}
      <div style={{ marginBottom: '30px' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: '300', marginBottom: '10px', color: '#2d3748' }}>
          Investment Portfolio
        </h1>
        <p style={{ color: '#718096', fontSize: '1.1rem' }}>Track your investments across different asset classes</p>
      </div>

      {/* Portfolio Summary */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        borderRadius: '20px',
        padding: '30px',
        marginBottom: '30px',
        boxShadow: '0 15px 35px rgba(0, 0, 0, 0.1)',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '20px'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#38a169', marginBottom: '5px' }}>
            {formatCurrency(412156)}
          </div>
          <div style={{ color: '#718096', fontSize: '0.9rem' }}>Total Portfolio Value</div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#667eea', marginBottom: '5px' }}>
            +23.4%
          </div>
          <div style={{ color: '#718096', fontSize: '0.9rem' }}>Overall Returns</div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#f59e0b', marginBottom: '5px' }}>
            4
          </div>
          <div style={{ color: '#718096', fontSize: '0.9rem' }}>Asset Classes</div>
        </div>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#8b5cf6', marginBottom: '5px' }}>
            12
          </div>
          <div style={{ color: '#718096', fontSize: '0.9rem' }}>Total Holdings</div>
        </div>
      </div>

      {/* Portfolio Categories */}
      <div style={{ display: 'grid', gap: '30px' }}>
        {portfolioData.map((category, categoryIndex) => (
          <div key={categoryIndex} style={{
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
              marginBottom: '20px',
              paddingBottom: '15px',
              borderBottom: '1px solid #e2e8f0'
            }}>
              <h2 style={{ fontSize: '1.5rem', fontWeight: '600', color: '#2d3748', margin: 0 }}>
                {category.category}
              </h2>
              <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#38a169' }}>
                {formatCurrency(category.totalValue)}
              </div>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
              gap: '20px'
            }}>
              {category.holdings.map((holding, holdingIndex) => (
                <div key={holdingIndex} style={{
                  background: '#f8fafc',
                  borderRadius: '12px',
                  padding: '20px',
                  border: '1px solid #e2e8f0'
                }}>
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start',
                    marginBottom: '15px'
                  }}>
                    <div style={{
                      fontWeight: '600',
                      color: '#2d3748',
                      fontSize: '1rem',
                      lineHeight: '1.3'
                    }}>
                      {holding.name}
                    </div>
                    <div style={{
                      fontWeight: 'bold',
                      color: '#38a169',
                      fontSize: '1.1rem'
                    }}>
                      {formatCurrency(holding.value)}
                    </div>
                  </div>

                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: '1fr 1fr',
                    gap: '10px',
                    fontSize: '0.9rem',
                    color: '#4a5568'
                  }}>
                    {Object.entries(holding).map(([key, value], idx) => {
                      if (key === 'name' || key === 'value') return null;
                      
                      let label = key;
                      let displayValue = value;
                      
                      switch (key) {
                        case 'units':
                          label = 'Units';
                          displayValue = typeof value === 'number' ? value.toFixed(2) : value;
                          break;
                        case 'nav':
                          label = 'NAV';
                          displayValue = typeof value === 'number' ? formatCurrency(value) : value;
                          break;
                        case 'quantity':
                          label = 'Quantity';
                          displayValue = `${value} shares`;
                          break;
                        case 'ltp':
                          label = 'Last Price';
                          displayValue = typeof value === 'number' ? formatCurrency(value) : value;
                          break;
                        case 'returns':
                          label = 'Absolute Returns';
                          displayValue = typeof value === 'number' ? formatCurrency(value) : value;
                          break;
                        case 'returnsPercent':
                          label = 'Returns %';
                          displayValue = typeof value === 'number' ? formatPercent(value) : value;
                          break;
                        case 'closingRate':
                          label = 'Closing Rate';
                          displayValue = typeof value === 'number' ? `₹${value}` : value;
                          break;
                        default:
                          label = key.charAt(0).toUpperCase() + key.slice(1);
                      }
                      
                      return (
                        <div key={idx} style={{ display: 'flex', justifyContent: 'space-between' }}>
                          <span style={{ color: '#718096' }}>{label}:</span>
                          <span style={{ 
                            fontWeight: '500',
                            color: key === 'returns' || key === 'returnsPercent' ? '#38a169' : '#2d3748'
                          }}>
                            {displayValue}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}; 