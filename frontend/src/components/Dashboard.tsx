import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

export const Dashboard: React.FC = () => {
  // Assets data
  const assetsData = {
    labels: ['Savings Accounts', 'EPF', 'Indian Stocks', 'Mutual Funds', 'US Securities'],
    datasets: [{
      data: [740841, 211111, 200642, 177605, 31086],
      backgroundColor: [
        '#4F46E5',
        '#10B981',
        '#F59E0B',
        '#EF4444',
        '#8B5CF6'
      ],
      borderWidth: 0
    }]
  };

  // Liabilities data
  const liabilitiesData = {
    labels: ['Other Loan', 'Home Loan', 'Vehicle Loan'],
    datasets: [{
      data: [42000, 17000, 5000],
      backgroundColor: [
        '#DC2626',
        '#F97316',
        '#EAB308'
      ],
      borderWidth: 0
    }]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      }
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const Legend: React.FC<{ data: any }> = ({ data }) => (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '15px', justifyContent: 'center' }}>
      {data.labels.map((label: string, index: number) => (
        <div key={index} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div
            style={{
              width: '12px',
              height: '12px',
              borderRadius: '50%',
              backgroundColor: data.datasets[0].backgroundColor[index]
            }}
          />
          <span style={{ fontSize: '0.9rem', color: '#4a5568' }}>{label}</span>
        </div>
      ))}
    </div>
  );

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '20px' }}>
      {/* Header */}
      <div style={{ textAlign: 'center', marginBottom: '40px', color: 'white' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: '300', marginBottom: '10px', color: '#2d3748' }}>
          Net Worth Dashboard
        </h1>
        <p style={{ color: '#718096' }}>Your complete financial overview</p>
      </div>

      {/* Net Worth Card */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        borderRadius: '20px',
        padding: '30px',
        marginBottom: '30px',
        boxShadow: '0 20px 40px rgba(0, 0, 0, 0.1)',
        textAlign: 'center'
      }}>
        <div style={{ fontSize: '3rem', fontWeight: 'bold', color: '#2d3748', marginBottom: '10px' }}>
          ₹12,97,285
        </div>
        <div style={{
          fontSize: '1.2rem',
          color: '#718096',
          textTransform: 'uppercase',
          letterSpacing: '1px'
        }}>
          Total Net Worth
        </div>
      </div>

      {/* Dashboard Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))',
        gap: '30px',
        marginBottom: '30px'
      }}>
        {/* Assets Chart */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(10px)',
          borderRadius: '20px',
          padding: '25px',
          boxShadow: '0 15px 35px rgba(0, 0, 0, 0.1)'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: '20px'
          }}>
            <div style={{ fontSize: '1.4rem', fontWeight: '600', color: '#2d3748' }}>
              Asset Allocation
            </div>
            <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#4a5568' }}>
              ₹13,61,285
            </div>
          </div>
          <div style={{ position: 'relative', height: '300px', marginBottom: '20px' }}>
            <Doughnut data={assetsData} options={chartOptions} />
          </div>
          <Legend data={assetsData} />
        </div>

        {/* Liabilities Chart */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(10px)',
          borderRadius: '20px',
          padding: '25px',
          boxShadow: '0 15px 35px rgba(0, 0, 0, 0.1)'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: '20px'
          }}>
            <div style={{ fontSize: '1.4rem', fontWeight: '600', color: '#2d3748' }}>
              Liabilities
            </div>
            <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#e53e3e' }}>
              ₹64,000
            </div>
          </div>
          <div style={{ position: 'relative', height: '300px', marginBottom: '20px' }}>
            <Doughnut data={liabilitiesData} options={chartOptions} />
          </div>
          <Legend data={liabilitiesData} />
        </div>

        {/* Bank Accounts */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(10px)',
          borderRadius: '20px',
          padding: '25px',
          boxShadow: '0 15px 35px rgba(0, 0, 0, 0.1)'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: '20px'
          }}>
            <div style={{ fontSize: '1.4rem', fontWeight: '600', color: '#2d3748' }}>
              Bank Accounts
            </div>
            <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#4a5568' }}>
              ₹7,40,841
            </div>
          </div>
          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            {[
              { name: 'HDFC Bank Savings', number: 'XXXXXX9026', balance: 5225 },
              { name: 'Union Bank Current', number: 'XXXXXX2997', balance: 109232 },
              { name: 'Union Bank Savings', number: 'XXXXXX2992', balance: 106207 },
              { name: 'IDFC Bank Savings', number: 'XXXXXX5350', balance: 108662 },
              { name: 'Union Bank Savings', number: 'XXXXXX8235', balance: 108438 },
              { name: 'IDFC Bank Savings', number: 'XXXXXX6750', balance: 105535 }
            ].map((account, index) => (
              <div key={index} style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '15px 0',
                borderBottom: index < 5 ? '1px solid #e2e8f0' : 'none'
              }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: '500', color: '#2d3748', marginBottom: '5px' }}>
                    {account.name}
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#a0aec0' }}>
                    {account.number}
                  </div>
                </div>
                <div style={{ fontWeight: 'bold', color: '#2d3748' }}>
                  {formatCurrency(account.balance)}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Investment Performance */}
        <div style={{
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(10px)',
          borderRadius: '20px',
          padding: '25px',
          boxShadow: '0 15px 35px rgba(0, 0, 0, 0.1)'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: '20px'
          }}>
            <div style={{ fontSize: '1.4rem', fontWeight: '600', color: '#2d3748' }}>
              Investment Performance
            </div>
          </div>
          {[
            { label: 'Total Assets', value: 1361285, positive: true },
            { label: 'Total Liabilities', value: 64000, positive: false },
            { label: 'Mutual Funds', value: 177605, positive: true },
            { label: 'Indian Stocks', value: 200642, positive: true },
            { label: 'US Securities', value: 31086, positive: true },
            { label: 'EPF Balance', value: 211111, positive: true }
          ].map((metric, index) => (
            <div key={index} style={{
              display: 'flex',
              justifyContent: 'space-between',
              margin: '10px 0',
              padding: '8px 0',
              borderBottom: index < 5 ? '1px solid #f0f0f0' : 'none'
            }}>
              <span style={{ color: '#718096', fontSize: '0.9rem' }}>
                {metric.label}
              </span>
              <span style={{
                fontWeight: '600',
                color: metric.positive ? '#38a169' : '#e53e3e'
              }}>
                {formatCurrency(metric.value)}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Holdings Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
        gap: '20px'
      }}>
        {[
          {
            name: 'ICICI Prudential Nifty 50 Index Fund',
            value: 177605,
            details: {
              invested: 10027,
              nav: 267.69,
              units: 665.02,
              returns: 167578,
              xirr: '136.63%'
            }
          },
          {
            name: 'HDFC Bank Limited',
            value: 19500,
            details: {
              quantity: '12 shares',
              ltp: 1625,
              isin: 'INE040A01034'
            }
          },
          {
            name: 'Brookfield India REIT',
            value: 1673,
            details: {
              units: 115,
              closingRate: 14.55,
              type: 'REIT'
            }
          },
          {
            name: 'PowerGrid Infrastructure InvIT',
            value: 1150,
            details: {
              units: 115,
              type: 'InvIT',
              isin: 'INE0GGX23010'
            }
          }
        ].map((holding, index) => (
          <div key={index} style={{
            background: 'rgba(255, 255, 255, 0.95)',
            borderRadius: '15px',
            padding: '20px',
            boxShadow: '0 10px 25px rgba(0, 0, 0, 0.08)'
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
                fontSize: '1rem'
              }}>
                {holding.name}
              </div>
              <div style={{
                fontWeight: 'bold',
                color: '#38a169'
              }}>
                {formatCurrency(holding.value)}
              </div>
            </div>
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '10px',
              fontSize: '0.9rem',
              color: '#718096'
            }}>
              {Object.entries(holding.details).map(([key, value], idx) => (
                <div key={idx} style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ textTransform: 'capitalize' }}>{key.replace(/([A-Z])/g, ' $1')}:</span>
                  <span>{typeof value === 'number' ? formatCurrency(value) : value}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}; 