import React, { useState, useEffect } from 'react';
import { Dashboard } from './components/Dashboard';
import { Sidebar } from './components/Sidebar';
import { HamburgerMenu } from './components/HamburgerMenu';
import { FloatingChat } from './components/FloatingChat';
import { Portfolio } from './components/pages/Portfolio';
import { Transactions } from './components/pages/Transactions';
import { GoalPlanner } from './components/pages/GoalPlanner';
import { PlaceholderPage } from './components/pages/PlaceholderPage';
import { Login } from './components/Login';
import { Register } from './components/Register';
import { UserProfile } from './components/UserProfile';
import { authService } from './services/authService';

type AuthState = 'loading' | 'login' | 'register' | 'authenticated';

function App() {
  const [authState, setAuthState] = useState<AuthState>('loading');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  useEffect(() => {
    // Listen to Firebase Auth state changes
    const unsubscribe = authService.onAuthStateChanged((user) => {
      console.log("Firebase Auth state changed:", user);

      if (user && authService.isAuthenticated()) {
        // User is signed in to Firebase and has local auth token
        setIsAuthenticated(true);
        setAuthState('authenticated');
      } else {
        // User is not signed in or no local auth token
        setIsAuthenticated(false);
        setAuthState('login');
        setCurrentPage('dashboard');

        // Clear any stale data
        authService.removeToken();
      }
    });

    // Initial check for existing authentication - wait for Firebase to be ready
    const initialCheck = async () => {
      try {
        // Wait for Firebase Auth to be fully initialized
        const isAuthenticated = await authService.waitForAuthReady();

        console.log("Initial auth check result:", isAuthenticated);

        if (isAuthenticated) {
          setIsAuthenticated(true);
          setAuthState('authenticated');
        } else {
          setIsAuthenticated(false);
          setAuthState('login');
          // Clean up any inconsistent state
          authService.removeToken();
        }
      } catch (error) {
        console.error("Error during initial auth check:", error);
        setIsAuthenticated(false);
        setAuthState('login');
        authService.removeToken();
      }
    };

    // Run initial check
    initialCheck();

    // Cleanup subscription on unmount
    return () => unsubscribe();
  }, []);

  const handleLoginSuccess = () => {
    console.log("Login success handler called");
    setIsAuthenticated(true);
    setAuthState('authenticated');
  };

  const handleRegisterSuccess = () => {
    console.log("Register success handler called");
    setIsAuthenticated(true);
    setAuthState('authenticated');
  };

  const handleLogout = async () => {
    console.log("Logout handler called");

    try {
      await authService.logout();
      console.log("Logout successful");
    } catch (error) {
      console.error("Logout error:", error);
    }

    // State will be updated by the onAuthStateChanged listener
    // But we can also update it here for immediate UI feedback
    setIsAuthenticated(false);
    setAuthState('login');
    setCurrentPage('dashboard');
    setSidebarOpen(false);
  };

  const handlePageChange = (page: string) => {
    if (page === 'signout') {
      handleLogout();
      return;
    }
    setCurrentPage(page);
  };

  const handleChatMessage = (message: string) => {
    console.log('Chat message:', message);
    // TODO: Integrate with chat service
  };

  const renderAuthContent = () => {
    if (authState === 'loading') {
      return (
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
          fontSize: '1.2rem',
          color: '#666'
        }}>
          Loading...
        </div>
      );
    }

    switch (authState) {
      case 'login':
        return (
          <Login
            onLoginSuccess={handleLoginSuccess}
            onSwitchToRegister={() => setAuthState('register')}
          />
        );
      case 'register':
        return (
          <Register
            onRegisterSuccess={handleRegisterSuccess}
            onSwitchToLogin={() => setAuthState('login')}
          />
        );
      default:
        return null;
    }
  };

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;
      case 'portfolio':
        return <Portfolio />;
      case 'transactions':
        return <Transactions />;
      case 'goal-planner':
        return <GoalPlanner />;
      case 'reports':
        return (
          <PlaceholderPage
            title="Scheduled Reports"
            description="AI-powered automated reports to keep you informed about your financial progress, market insights, and personalized recommendations delivered to your inbox."
            icon="📄"
          />
        );
      case 'advisor':
        return (
          <PlaceholderPage
            title="Investment Advisor"
            description="Get personalized investment recommendations based on your risk profile, financial goals, and market conditions using advanced AI algorithms."
            icon="✅"
          />
        );
      case 'tax-optimizer':
        return (
          <PlaceholderPage
            title="Tax Optimizer"
            description="Maximize your tax savings with AI-driven strategies for tax planning, investment optimization, and expense categorization."
            icon="📋"
          />
        );
      case 'profile':
        return <UserProfile />;
      case 'security':
        return (
          <PlaceholderPage
            title="Security & Privacy"
            description="Manage your account security settings, privacy preferences, and data sharing options to keep your financial information safe."
            icon="🛡️"
          />
        );
      case 'support':
        return (
          <PlaceholderPage
            title="Support & Help"
            description="Get assistance with any questions or issues. Access our knowledge base, contact support, or schedule a consultation with our financial experts."
            icon="📧"
          />
        );
      default:
        return <Dashboard />;
    }
  };

  const renderAuthenticatedContent = () => {
    return (
      <div style={{
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        minHeight: '100vh',
        color: '#333',
        paddingBottom: '100px'
      }}>
        {/* Hamburger Menu */}
        <HamburgerMenu
          isOpen={sidebarOpen}
          onToggle={() => setSidebarOpen(!sidebarOpen)}
        />

        {/* Sidebar */}
        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          currentPage={currentPage}
          onPageChange={handlePageChange}
          onToggleSidebar={toggleSidebar}
        />

        {/* Main Content */}
        <div style={{
          transition: 'margin-left 0.3s ease',
          marginLeft: sidebarOpen && window.innerWidth > 768 ? '0' : '0'
        }}>
          {renderCurrentPage()}
        </div>

        {/* Floating Chat */}
        <FloatingChat onSendMessage={handleChatMessage} />
      </div>
    );
  };

  // Show loading state while determining auth status
  if (authState === 'loading') {
    return (
      <div style={{
        fontFamily: 'Inter, sans-serif',
        background: '#F0F4F9',
        minHeight: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Talk to Your Money</div>
          <div style={{ color: '#666' }}>Loading...</div>
        </div>
      </div>
    );
  }

  return (
    <div>
      {isAuthenticated ? renderAuthenticatedContent() : (
        <div style={{
          fontFamily: 'Inter, sans-serif',
          background: '#F0F4F9',
          minHeight: '100vh',
          padding: 32
        }}>
          {renderAuthContent()}
        </div>
      )}
    </div>
  );
}

export default App;
