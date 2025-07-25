import React, { useState, useRef, useEffect } from 'react';

interface FloatingChatProps {
  onSendMessage?: (message: string) => void;
}

export const FloatingChat: React.FC<FloatingChatProps> = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');
  const [isVisible, setIsVisible] = useState(true);
  const [isMobileActive, setIsMobileActive] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const autoResize = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px';
    }
  };

  const handleSendMessage = () => {
    const trimmedMessage = message.trim();
    if (trimmedMessage) {
      onSendMessage?.(trimmedMessage);
      
      // Feedback
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.placeholder = 'Message sent! Ask another question...';
        textareaRef.current.style.height = 'auto';
      }
      
      // Reset placeholder after 3 seconds
      setTimeout(() => {
        if (textareaRef.current) {
          textareaRef.current.placeholder = 'Ask about your finances, investments, or get financial advice...';
        }
      }, 3000);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleMobileChat = () => {
    setIsMobileActive(!isMobileActive);
  };

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 480) {
        setIsVisible(true);
        setIsMobileActive(false);
      } else {
        setIsVisible(isMobileActive);
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize(); // Call once on mount

    return () => window.removeEventListener('resize', handleResize);
  }, [isMobileActive]);

  useEffect(() => {
    autoResize();
  }, [message]);

  return (
    <>
      {/* Main Chat Container */}
      <div
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          left: '20px',
          maxWidth: '600px',
          margin: '0 auto',
          zIndex: 1000,
          display: isVisible ? 'block' : 'none'
        }}
      >
        <div
          style={{
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(15px)',
            borderRadius: '25px',
            padding: window.innerWidth <= 768 ? '12px 15px' : '15px 20px',
            boxShadow: '0 10px 40px rgba(0, 0, 0, 0.15)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            display: 'flex',
            alignItems: 'center',
            gap: '15px',
            transition: 'all 0.3s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.boxShadow = '0 15px 50px rgba(0, 0, 0, 0.2)';
            e.currentTarget.style.transform = 'translateY(-2px)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.boxShadow = '0 10px 40px rgba(0, 0, 0, 0.15)';
            e.currentTarget.style.transform = 'translateY(0)';
          }}
        >
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about your finances, investments, or get financial advice..."
            style={{
              flex: 1,
              border: 'none',
              outline: 'none',
              background: 'transparent',
              fontSize: '16px',
              color: '#2d3748',
              fontFamily: 'inherit',
              resize: 'none',
              minHeight: '24px',
              maxHeight: '120px',
              lineHeight: '1.5'
            }}
            rows={1}
          />
          
          <button
            onClick={handleSendMessage}
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              border: 'none',
              borderRadius: '50%',
              width: window.innerWidth <= 768 ? '40px' : '45px',
              height: window.innerWidth <= 768 ? '40px' : '45px',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'all 0.3s ease',
              flexShrink: 0
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'scale(1.1)';
              e.currentTarget.style.boxShadow = '0 5px 20px rgba(102, 126, 234, 0.4)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'scale(1)';
              e.currentTarget.style.boxShadow = 'none';
            }}
            onMouseDown={(e) => {
              e.currentTarget.style.transform = 'scale(0.95)';
            }}
            onMouseUp={(e) => {
              e.currentTarget.style.transform = 'scale(1.1)';
            }}
          >
            <svg
              width={window.innerWidth <= 768 ? "18" : "20"}
              height={window.innerWidth <= 768 ? "18" : "20"}
              viewBox="0 0 24 24"
              fill="white"
            >
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Chat Toggle Button */}
      {window.innerWidth <= 480 && (
        <button
          onClick={toggleMobileChat}
          style={{
            position: 'fixed',
            bottom: '20px',
            right: '20px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            border: 'none',
            borderRadius: '50%',
            width: '55px',
            height: '55px',
            cursor: 'pointer',
            display: isVisible ? 'none' : 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 10px 30px rgba(0, 0, 0, 0.2)',
            transition: 'all 0.3s ease',
            zIndex: 1001
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'scale(1.1)';
            e.currentTarget.style.boxShadow = '0 15px 40px rgba(102, 126, 234, 0.4)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'scale(1)';
            e.currentTarget.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.2)';
          }}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
          </svg>
        </button>
      )}
    </>
  );
}; 