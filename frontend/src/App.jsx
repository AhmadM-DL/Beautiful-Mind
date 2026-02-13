
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import Register from './Register';
import Dashboard from './Dashboard';
import LandingPage from './LandingPage';

// Protected route component
const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem('access_token');
    const role = localStorage.getItem('user_role');

    if (!token || (role !== 'DOCTOR' && role !== 'PATIENT')) {
        return <Navigate to="/" replace />;
    }

    return children;
};

// Login route component that redirects if already logged in
const LoginRoute = () => {
    const token = localStorage.getItem('access_token');
    const role = localStorage.getItem('user_role');

    if (token && (role === 'DOCTOR' || role === 'PATIENT')) {
        return <Navigate to="/dashboard" replace />;
    }

    return <Login />;
};

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LoginRoute />} />
                <Route path="/register" element={<Register />} />
                <Route path="/info" element={<LandingPage />} />
                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;
