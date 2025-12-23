
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerDoctor } from './api';

const Register = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        password: ''
    });
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await registerDoctor(formData);
            navigate('/');
        } catch (err) {
            console.error(err);
            setError('Registration failed. Username may be taken.');
        }
    };

    return (
        <div className="register-container">
            <div className="register-box">
                <h2>Doctor Registration</h2>
                {error && <p className="error">{error}</p>}
                <form onSubmit={handleSubmit}>
                    {['username', 'first_name', 'last_name', 'phone_number'].map((field) => (
                        <div className="form-group" key={field}>
                            <input
                                type="text"
                                name={field}
                                value={formData[field]}
                                onChange={handleChange}
                                placeholder={field.replace('_', ' ').substring(0, 1).toUpperCase() + field.replace('_', ' ').substring(1)}
                                required
                            />
                        </div>
                    ))}
                    <div className="form-group">
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            placeholder="Password"
                            required
                        />
                    </div>
                    <div className="button-group">
                        <button type="submit" className="btn btn-primary">Register</button>
                        <button type="button" className="btn btn-text" onClick={() => navigate('/')}>Back to Login</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Register;
