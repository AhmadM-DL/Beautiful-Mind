
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerDoctor } from './api';
import CountryCodeSelect from './CountryCodeSelect';

const Register = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        password: ''
    });
    const [countryCode, setCountryCode] = useState('+1');
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const dataToSubmit = {
                ...formData,
                phone_number: countryCode + formData.phone_number
            };
            await registerDoctor(dataToSubmit);
            navigate('/');
        } catch (err) {
            console.error(err);
            setError(err.response?.data?.error || 'Registration failed.');
        }
    };

    return (
        <div className="register-container">
            <div className="register-box">
                <h2>Doctor Registration</h2>
                {error && <p className="error">{error}</p>}
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Username *</label>
                        <input
                            type="text"
                            name="username"
                            value={formData.username}
                            onChange={handleChange}
                            placeholder="Username"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>First Name *</label>
                        <input
                            type="text"
                            name="first_name"
                            value={formData.first_name}
                            onChange={handleChange}
                            placeholder="First Name"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Last Name *</label>
                        <input
                            type="text"
                            name="last_name"
                            value={formData.last_name}
                            onChange={handleChange}
                            placeholder="Last Name"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Phone Number *</label>
                        <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-end', marginTop: '5px' }}>
                            <CountryCodeSelect
                                value={countryCode}
                                onChange={setCountryCode}
                            />
                            <input
                                type="tel"
                                name="phone_number"
                                value={formData.phone_number}
                                onChange={handleChange}
                                placeholder="Phone Number"
                                required
                                style={{ flex: 1, marginTop: 0 }}
                            />
                        </div>
                    </div>
                    <div className="form-group">
                        <label>Password *</label>
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
