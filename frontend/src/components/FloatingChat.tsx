import React, { useState, useRef, useEffect, useMemo } from 'react';

interface FloatingChatProps {
  onSendMessage: (message: string) => void;
}

export const FloatingChat: React.FC<FloatingChatProps> = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');
  const [isVisible, setIsVisible] = useState(true);
  const [isMobileActive, setIsMobileActive] = useState(false);
  const [currentPromptIndex, setCurrentPromptIndex] = useState(0);
  const [animatedPlaceholder, setAnimatedPlaceholder] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [initialMessage, setInitialMessage] = useState<string>('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Array of rotating placeholder prompts
  const placeholderPrompts = useMemo(() => [
    "How much should I save each month?",
    "Is my spending on track this month?",
    "Can I take a vacation this year?",
    "How do I start investing?",
    "Am I financially ready for a baby?",
    "Should I buy or rent a home?",
    "What's my current financial health?",
    "How do I build an emergency fund?",
    "Is my credit score good?",
    "Can I retire by 55?",
    "What's the best use of my bonus?",
    "Should I increase my SIP amount?",
    "Is my insurance coverage sufficient?",
    "How much to save for child's education?",
    "Am I paying too much in fees?",
    "Can I afford a new car next year?",
    "How to optimize my monthly budget?",
    "Am I saving enough for retirement?",
    "Should I sell my mutual funds now?",
    "How to reduce my credit card debt?",
    "Can I take a home loan safely?",
    "How can I achieve financial independence early?",
    "Is my investment portfolio diversified enough?",
    "What should I do with idle money?",
    "How much should I spend on rent?"
  ], []);

  // Typing animation effect
  const animateTyping = (text: string) => {
    setIsTyping(true);
    setAnimatedPlaceholder('');

    const totalDuration = 1000; // 500ms total
    const characters = text.split('');
    const intervalTime = totalDuration / characters.length;

    let currentIndex = 0;

    const typingInterval = setInterval(() => {
      if (currentIndex < characters.length) {
        setAnimatedPlaceholder(characters.slice(0, currentIndex + 1).join(''));
        currentIndex++;
      } else {
        setAnimatedPlaceholder(text);
        clearInterval(typingInterval);
        setIsTyping(false);
      }
    }, intervalTime);

    return () => clearInterval(typingInterval);
  };

  // Rotate prompts every 3 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentPromptIndex((prevIndex) =>
        (prevIndex + 1) % placeholderPrompts.length
      );
    }, 3000);

    return () => clearInterval(interval);
  }, [placeholderPrompts.length]);

  // Animate typing when prompt changes
  useEffect(() => {
    const currentPrompt = placeholderPrompts[currentPromptIndex];
    const cleanup = animateTyping(currentPrompt);
    return cleanup;
  }, [currentPromptIndex, placeholderPrompts]);

  const autoResize = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px';
    }
  };

  const handleSendMessage = () => {
    const trimmedMessage = message.trim();
    if (trimmedMessage) {
      // Set the initial message and show the chat interface
      setInitialMessage(trimmedMessage);
      onSendMessage(trimmedMessage);

      // Clear the input
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    } else if (e.key === 'Tab') {
      e.preventDefault();
      // Fill the current placeholder prompt
      setMessage(placeholderPrompts[currentPromptIndex]);
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

  // Update placeholder when animated text changes
  useEffect(() => {
    if (textareaRef.current && !message) {
      textareaRef.current.placeholder = animatedPlaceholder;
    }
  }, [animatedPlaceholder, message]);



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
          <div style={{ flex: 1, position: 'relative' }}>
            <textarea
              ref={textareaRef}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              onKeyDown={(e) => {
                if (e.key === 'Tab') {
                  e.preventDefault();
                  setMessage(placeholderPrompts[currentPromptIndex]);
                }
              }}
              placeholder={animatedPlaceholder}
              style={{
                width: '100%',
                border: 'none',
                outline: 'none',
                background: 'transparent',
                fontSize: '16px',
                color: '#2d3748',
                fontFamily: 'inherit',
                resize: 'none',
                minHeight: '24px',
                maxHeight: '120px',
                lineHeight: '1.5',
                paddingRight: '30px'
              }}
              rows={1}
            />
          </div>

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
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
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
            <path d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z" />
          </svg>
        </button>
      )}
    </>
  );
}; 