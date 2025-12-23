
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from './api';

const Login = () => {
    const [identifier, setIdentifier] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const data = await login(identifier, password);
            // Assuming the backend returns role info, or we just try to nav to dashboard
            // If the user validates as a doctor, we go to dashboard.
            // The User request says "if login user role is a doctor... get all patients"
            navigate('/dashboard');
        } catch (err) {
            console.error(err);
            setError('Invalid credentials');
        }
    };

    return (
        <div className="login-container">
            <div className="login-header">BeautifulMind</div>
            <div className="login-box">
                <h2>Login</h2>
                {error && <p className="error">{error}</p>}
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <input
                            type="text"
                            value={identifier}
                            onChange={(e) => setIdentifier(e.target.value)}
                            placeholder="Phone number or username"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Password"
                            required
                        />
                    </div>
                    <div className="button-group">
                        <button type="submit" className="btn btn-primary">Login</button>
                        <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={() => navigate('/register')}
                        >
                            Register as a Doctor
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;
