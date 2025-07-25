import React, { useState } from 'react';

export const Transactions: React.FC = () => {
  const [filter, setFilter] = useState('all');
  const [dateRange, setDateRange] = useState('30');

  const transactions = [
    {
      id: 1,
      date: '2024-01-15',
      description: 'ICICI Prudential Nifty 50 - SIP',
      type: 'investment',
      category: 'Mutual Fund',
      amount: -5000,
      balance: 740841
    },
    {
      id: 2,
      date: '2024-01-14',
      description: 'Salary Credit',
      type: 'income',
      category: 'Salary',
      amount: 125000,
      balance: 745841
    },
    {
      id: 3,
      date: '2024-01-12',
      description: 'HDFC Bank - Dividend',
      type: 'income',
      category: 'Dividend',
      amount: 480,
      balance: 620841
    },
    {
      id: 4,
      date: '2024-01-10',
      description: 'Grocery Shopping',
      type: 'expense',
      category: 'Food & Dining',
      amount: -3500,
      balance: 620361
    },
    {
      id: 5,
      date: '2024-01-08',
      description: 'Apple Inc. - Buy Order',
      type: 'investment',
      category: 'US Stocks',
      amount: -25000,
      balance: 623861
    },
    {
      id: 6,
      date: '2024-01-05',
      description: 'Rent Payment',
      type: 'expense',
      category: 'Housing',
      amount: -35000,
      balance: 648861
    },
    {
      id: 7,
      date: '2024-01-03',
      description: 'Reliance Industries - Buy',
      type: 'investment',
      category: 'Indian Stocks',
      amount: -42000,
      balance: 683861
    },
    {
      id: 8,
      date: '2024-01-01',
      description: 'Interest Credit - Savings Account',
      type: 'income',
      category: 'Interest',
      amount: 1250,
      balance: 725861
    }
  ];

  const filteredTransactions = transactions.filter(transaction => {
    if (filter === 'all') return true;
    return transaction.type === filter;
  });

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0
    }).format(Math.abs(amount));
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'income': return '#38a169';
      case 'expense': return '#e53e3e';
      case 'investment': return '#667eea';
      default: return '#4a5568';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'income': return '💰';
      case 'expense': return '💸';
      case 'investment': return '📈';
      default: return '💳';
    }
  };

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '20px' }}>
      {/* Header */}
      <div style={{ marginBottom: '30px' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: '300', marginBottom: '10px', color: '#2d3748' }}>
          Transactions
        </h1>
        <p style={{ color: '#718096', fontSize: '1.1rem' }}>Track all your financial transactions</p>
      </div>

      {/* Summary Cards */}
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
          <div style={{ fontSize: '1.8rem', fontWeight: 'bold', color: '#38a169', marginBottom: '5px' }}>
            ₹1,26,730
          </div>
          <div style={{ color: '#718096', fontSize: '0.9rem' }}>Total Income</div>
        </div>
        
        <div style={{
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(10px)',
          borderRadius: '15px',
          padding: '20px',
          boxShadow: '0 10px 25px rgba(0, 0, 0, 0.08)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '1.8rem', fontWeight: 'bold', color: '#e53e3e', marginBottom: '5px' }}>
            ₹38,500
          </div>
          <div style={{ color: '#718096', fontSize: '0.9rem' }}>Total Expenses</div>
        </div>
        
        <div style={{
          background: 'rgba(255, 255, 255, 0.95)',
          backdropFilter: 'blur(10px)',
          borderRadius: '15px',
          padding: '20px',
          boxShadow: '0 10px 25px rgba(0, 0, 0, 0.08)',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '1.8rem', fontWeight: 'bold', color: '#667eea', marginBottom: '5px' }}>
            ₹72,000
          </div>
          <div style={{ color: '#718096', fontSize: '0.9rem' }}>Investments</div>
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
            ₹16,230
          </div>
          <div style={{ color: '#718096', fontSize: '0.9rem' }}>Net Savings</div>
        </div>
      </div>

      {/* Filters */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        borderRadius: '15px',
        padding: '20px',
        marginBottom: '20px',
        boxShadow: '0 10px 25px rgba(0, 0, 0, 0.08)',
        display: 'flex',
        gap: '20px',
        alignItems: 'center',
        flexWrap: 'wrap'
      }}>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <span style={{ color: '#718096', fontSize: '0.9rem', fontWeight: '500' }}>Filter:</span>
          {['all', 'income', 'expense', 'investment'].map((type) => (
            <button
              key={type}
              onClick={() => setFilter(type)}
              style={{
                background: filter === type ? '#667eea' : 'transparent',
                color: filter === type ? 'white' : '#4a5568',
                border: filter === type ? 'none' : '1px solid #e2e8f0',
                borderRadius: '8px',
                padding: '8px 16px',
                cursor: 'pointer',
                fontSize: '0.9rem',
                fontWeight: '500',
                textTransform: 'capitalize',
                transition: 'all 0.2s ease'
              }}
            >
              {type}
            </button>
          ))}
        </div>
        
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <span style={{ color: '#718096', fontSize: '0.9rem', fontWeight: '500' }}>Period:</span>
          <select
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            style={{
              border: '1px solid #e2e8f0',
              borderRadius: '8px',
              padding: '8px 12px',
              fontSize: '0.9rem',
              background: 'white',
              color: '#4a5568'
            }}
          >
            <option value="7">Last 7 days</option>
            <option value="30">Last 30 days</option>
            <option value="90">Last 3 months</option>
            <option value="365">Last year</option>
          </select>
        </div>
      </div>

      {/* Transactions List */}
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        borderRadius: '20px',
        padding: '25px',
        boxShadow: '0 15px 35px rgba(0, 0, 0, 0.1)'
      }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: '600', color: '#2d3748', marginBottom: '20px' }}>
          Recent Transactions ({filteredTransactions.length})
        </h2>
        
        <div style={{ display: 'grid', gap: '15px' }}>
          {filteredTransactions.map((transaction) => (
            <div key={transaction.id} style={{
              display: 'flex',
              alignItems: 'center',
              padding: '15px',
              border: '1px solid #e2e8f0',
              borderRadius: '12px',
              background: '#f8fafc',
              transition: 'all 0.2s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#f1f5f9';
              e.currentTarget.style.borderColor = '#cbd5e1';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = '#f8fafc';
              e.currentTarget.style.borderColor = '#e2e8f0';
            }}
            >
              <div style={{
                fontSize: '2rem',
                marginRight: '15px'
              }}>
                {getTypeIcon(transaction.type)}
              </div>
              
              <div style={{ flex: 1 }}>
                <div style={{
                  fontWeight: '600',
                  color: '#2d3748',
                  marginBottom: '5px'
                }}>
                  {transaction.description}
                </div>
                <div style={{
                  fontSize: '0.9rem',
                  color: '#718096',
                  display: 'flex',
                  gap: '15px'
                }}>
                  <span>{new Date(transaction.date).toLocaleDateString('en-IN')}</span>
                  <span>•</span>
                  <span>{transaction.category}</span>
                </div>
              </div>
              
              <div style={{ textAlign: 'right' }}>
                <div style={{
                  fontSize: '1.1rem',
                  fontWeight: 'bold',
                  color: transaction.amount > 0 ? '#38a169' : getTypeColor(transaction.type),
                  marginBottom: '5px'
                }}>
                  {transaction.amount > 0 ? '+' : '-'}{formatCurrency(transaction.amount)}
                </div>
                <div style={{
                  fontSize: '0.8rem',
                  color: '#a0aec0'
                }}>
                  Balance: {formatCurrency(transaction.balance)}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}; 