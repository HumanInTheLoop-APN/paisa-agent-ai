import React from 'react';

interface HamburgerMenuProps {
  isOpen: boolean;
  onToggle: () => void;
}

export const HamburgerMenu: React.FC<HamburgerMenuProps> = ({ isOpen, onToggle }) => {
  return (
    <button
      onClick={onToggle}
      style={{
        position: 'fixed',
        top: '20px',
        left: '20px',
        background: 'rgba(255, 255, 255, 0.9)',
        backdropFilter: 'blur(10px)',
        border: 'none',
        borderRadius: '12px',
        width: '50px',
        height: '50px',
        cursor: 'pointer',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxShadow: '0 5px 20px rgba(0, 0, 0, 0.1)',
        zIndex: 1001,
        transition: 'all 0.3s ease'
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.background = 'rgba(255, 255, 255, 1)';
        e.currentTarget.style.transform = 'scale(1.05)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.background = 'rgba(255, 255, 255, 0.9)';
        e.currentTarget.style.transform = 'scale(1)';
      }}
    >
      <div style={{
        width: '20px',
        height: '16px',
        position: 'relative'
      }}>
        <span style={{
          display: 'block',
          height: '2px',
          width: '100%',
          background: '#4a5568',
          borderRadius: '1px',
          position: 'absolute',
          top: isOpen ? '7px' : '0',
          transform: isOpen ? 'rotate(45deg)' : 'rotate(0)',
          transition: 'all 0.3s ease'
        }} />
        <span style={{
          display: 'block',
          height: '2px',
          width: '100%',
          background: '#4a5568',
          borderRadius: '1px',
          position: 'absolute',
          top: '7px',
          opacity: isOpen ? 0 : 1,
          transition: 'all 0.3s ease'
        }} />
        <span style={{
          display: 'block',
          height: '2px',
          width: '100%',
          background: '#4a5568',
          borderRadius: '1px',
          position: 'absolute',
          top: isOpen ? '7px' : '14px',
          transform: isOpen ? 'rotate(-45deg)' : 'rotate(0)',
          transition: 'all 0.3s ease'
        }} />
      </div>
    </button>
  );
}; 