
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
            // Check if the user is a doctor
            if (data.role === 'DOCTOR') {
                navigate('/dashboard');
            } else {
                setError('Only doctors can access this portal');
                localStorage.removeItem('access_token');
                localStorage.removeItem('user_role');
                localStorage.removeItem('username');
            }
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
