import React from 'react';

interface PlaceholderPageProps {
  title: string;
  description: string;
  icon: string;
  comingSoon?: boolean;
}

export const PlaceholderPage: React.FC<PlaceholderPageProps> = ({ 
  title, 
  description, 
  icon, 
  comingSoon = true 
}) => {
  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '20px' }}>
      <div style={{
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(10px)',
        borderRadius: '20px',
        padding: '60px 40px',
        boxShadow: '0 15px 35px rgba(0, 0, 0, 0.1)',
        textAlign: 'center',
        minHeight: '400px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        <div style={{ fontSize: '4rem', marginBottom: '20px' }}>
          {icon}
        </div>
        
        <h1 style={{
          fontSize: '2.5rem',
          fontWeight: '300',
          marginBottom: '15px',
          color: '#2d3748'
        }}>
          {title}
        </h1>
        
        <p style={{
          color: '#718096',
          fontSize: '1.2rem',
          marginBottom: '30px',
          maxWidth: '600px',
          lineHeight: '1.6'
        }}>
          {description}
        </p>
        
        {comingSoon && (
          <div style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            padding: '12px 24px',
            borderRadius: '25px',
            fontSize: '1rem',
            fontWeight: '500',
            marginBottom: '20px'
          }}>
            🚀 Coming Soon
          </div>
        )}
        
        <p style={{
          color: '#a0aec0',
          fontSize: '0.9rem',
          fontStyle: 'italic'
        }}>
          This feature is currently under development and will be available in a future update.
        </p>
      </div>
    </div>
  );
}; 