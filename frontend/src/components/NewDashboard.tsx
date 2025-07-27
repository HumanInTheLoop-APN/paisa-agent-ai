import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid, ComposedChart, Line } from 'recharts';
import { TrendingUp, TrendingDown, CreditCard, PiggyBank, Briefcase, Home, Car, AlertCircle } from 'lucide-react';

const NetWorthDashboard = () => {
  // Net worth data
  const totalAssets = 575250;
  const totalLiabilities = 572000;
  const netWorth = 3250;

  // Asset breakdown
  const assetData = [
    { name: 'Mutual Funds', value: 435250, icon: TrendingUp, color: '#3B82F6' },
    { name: 'EPF (Retirement)', value: 115000, icon: PiggyBank, color: '#10B981' },
    { name: 'Savings Account', value: 25000, icon: Briefcase, color: '#F59E0B' },
  ];

  // Liability breakdown
  const liabilityData = [
    { name: 'Vehicle Loan', value: 542000, icon: Car, color: '#EF4444' },
    { name: 'Credit Cards', value: 30000, icon: CreditCard, color: '#F97316' },
  ];

  // Credit card details
  const creditCards = [
    { bank: 'SBI', balance: 18000, limit: 120000, utilization: 15 },
    { bank: 'ICICI', balance: 12000, limit: 80000, utilization: 15 },
  ];

  // Mutual fund performance
  const mutualFunds = [
    { name: 'SBI Bluechip Fund', invested: 40000, current: 84300, returns: 44300, xirr: 15.21 },
    { name: 'Kotak Flexi Cap Fund', invested: 25000, current: 54840, returns: 29840, xirr: 17.55 },
    { name: 'Axis Long Term Equity (Tax Saver)', invested: 150000, current: 296110, returns: 146110, xirr: 16.89 },
  ];

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  const CustomTooltip = ({ active, payload }: { active: boolean, payload: any }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 shadow-lg rounded-lg border">
          <p className="font-semibold">{payload[0].name}</p>
          <p className="text-sm">{formatCurrency(payload[0].value)}</p>
          <p className="text-xs text-gray-500">
            {((payload[0].value / (payload[0].payload.total || totalAssets)) * 100).toFixed(1)}% of total
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Your Financial Health Dashboard</h1>

      {/* Net Worth Overview */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">Net Worth Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Assets</p>
                <p className="text-2xl font-bold text-blue-600">{formatCurrency(totalAssets)}</p>
              </div>
              <TrendingUp className="w-8 h-8 text-blue-500" />
            </div>
          </div>

          <div className="bg-red-50 p-4 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Liabilities</p>
                <p className="text-2xl font-bold text-red-600">{formatCurrency(totalLiabilities)}</p>
              </div>
              <TrendingDown className="w-8 h-8 text-red-500" />
            </div>
          </div>

          <div className={`${netWorth > 0 ? 'bg-green-50' : 'bg-orange-50'} p-4 rounded-lg`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Net Worth</p>
                <p className={`text-2xl font-bold ${netWorth > 0 ? 'text-green-600' : 'text-orange-600'}`}>
                  {formatCurrency(netWorth)}
                </p>
              </div>
              {netWorth > 0 ? (
                <PiggyBank className="w-8 h-8 text-green-500" />
              ) : (
                <AlertCircle className="w-8 h-8 text-orange-500" />
              )}
            </div>
          </div>
        </div>

        {netWorth < 50000 && (
          <div className="mt-4 p-4 bg-yellow-50 rounded-lg flex items-start">
            <AlertCircle className="w-5 h-5 text-yellow-600 mr-2 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm text-yellow-800">
                <strong>Financial Alert:</strong> Your liabilities are almost equal to your assets.
                Consider focusing on paying down debt to improve your financial health.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Assets and Liabilities Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        {/* Assets Pie Chart */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Where Your Money Is</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={assetData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent as any * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {assetData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip active={true} payload={[]} />} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 space-y-2">
            {assetData.map((asset, index) => (
              <div key={index} className="flex items-center justify-between text-sm">
                <div className="flex items-center">
                  <div className={`w-3 h-3 rounded-full mr-2`} style={{ backgroundColor: asset.color }}></div>
                  <span>{asset.name}</span>
                </div>
                <span className="font-semibold">{formatCurrency(asset.value)}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Liabilities Pie Chart */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">What You Owe</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={liabilityData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent as any * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {liabilityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip active={true} payload={[]} />} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 space-y-2">
            {liabilityData.map((liability, index) => (
              <div key={index} className="flex items-center justify-between text-sm">
                <div className="flex items-center">
                  <div className={`w-3 h-3 rounded-full mr-2`} style={{ backgroundColor: liability.color }}></div>
                  <span>{liability.name}</span>
                </div>
                <span className="font-semibold">{formatCurrency(liability.value)}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Credit Card Analysis */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">Credit Card Health Check</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {creditCards.map((card, index) => (
            <div key={index} className="border rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-lg">{card.bank} Card</h3>
                <CreditCard className="w-6 h-6 text-gray-400" />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Current Balance:</span>
                  <span className="font-semibold">{formatCurrency(card.balance)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Credit Limit:</span>
                  <span>{formatCurrency(card.limit)}</span>
                </div>
                <div className="mt-3">
                  <div className="flex justify-between text-xs mb-1">
                    <span>Utilization</span>
                    <span className={card.utilization > 30 ? 'text-red-600 font-semibold' : 'text-green-600 font-semibold'}>
                      {card.utilization}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${card.utilization > 30 ? 'bg-red-500' : 'bg-green-500'
                        }`}
                      style={{ width: `${card.utilization}%` }}
                    ></div>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    {card.utilization <= 30 ? '✅ Good! Keep it below 30%' : '⚠️ Try to reduce usage'}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-800">
            <strong>💡 Tip:</strong> Keeping credit card usage below 30% of your limit helps improve your credit score!
          </p>
        </div>
      </div>

      {/* Investment Performance */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">Your Investments Performance</h2>
        <div className="space-y-4">
          {mutualFunds.map((fund, index) => (
            <div key={index} className="border rounded-lg p-4">
              <h3 className="font-semibold mb-3">{fund.name}</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                <div>
                  <p className="text-gray-600">Invested</p>
                  <p className="font-semibold">{formatCurrency(fund.invested)}</p>
                </div>
                <div>
                  <p className="text-gray-600">Current Value</p>
                  <p className="font-semibold text-green-600">{formatCurrency(fund.current)}</p>
                </div>
                <div>
                  <p className="text-gray-600">Profit</p>
                  <p className="font-semibold text-green-600">+{formatCurrency(fund.returns)}</p>
                </div>
                <div>
                  <p className="text-gray-600">Annual Return</p>
                  <p className="font-semibold text-green-600">{fund.xirr}%</p>
                </div>
              </div>
              <div className="mt-3">
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="h-2 rounded-full bg-green-500"
                    style={{ width: `${Math.min((fund.returns / fund.invested) * 100, 100)}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {((fund.returns / fund.invested) * 100).toFixed(0)}% total gain
                </p>
              </div>
            </div>
          ))}
        </div>
        <div className="mt-4 p-4 bg-green-50 rounded-lg">
          <p className="text-sm text-green-800">
            <strong>🎯 Great Job!</strong> Your investments are performing well with an average return of ~16% annually!
          </p>
        </div>
      </div>
    </div>
  );
};

export default NetWorthDashboard;