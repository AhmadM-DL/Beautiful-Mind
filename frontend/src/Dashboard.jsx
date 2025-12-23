
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPatients, createPatient, updatePatient } from './api';
import CountryCodeSelect from './CountryCodeSelect';
import './Dashboard.css';

const Dashboard = () => {
    const navigate = useNavigate();
    const [patients, setPatients] = useState([]);
    const [isAddMode, setIsAddMode] = useState(false);
    const [editingPatient, setEditingPatient] = useState(null); // null means no patient selected for edit
    const [error, setError] = useState(''); // Error message state
    const [countryCode, setCountryCode] = useState('+1'); // Country code for phone number

    // New patient / Edit patient form state
    const [formData, setFormData] = useState({
        patient_phone_number: '', // For creation only, hashed on backend
        alias: '',
        gender: '',
        age: '',
        married: 'false',
        mental_illness_diagnostic: '',
        medications: '',
        smoke: 'false',
        weekly_sport_activity: '',
        occupation: ''
    });

    useEffect(() => {
        loadPatients();
    }, []);

    const loadPatients = async () => {
        try {
            const data = await getPatients();
            setPatients(data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_role');
        localStorage.removeItem('username');
        navigate('/');
    };

    const handleInputChange = (e) => {
        const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
        setFormData({ ...formData, [e.target.name]: value });
    };

    const resetForm = () => {
        setFormData({
            patient_phone_number: '',
            alias: '',
            gender: '',
            age: '',
            married: 'false',
            mental_illness_diagnostic: '',
            medications: '',
            smoke: 'false',
            weekly_sport_activity: '',
            occupation: ''
        });
        setIsAddMode(false);
        setEditingPatient(null);
        setError(''); // Clear error when resetting form
    };

    const handleAddClick = () => {
        resetForm();
        setIsAddMode(true);
        setError(''); // Clear any previous errors
    };

    const handlePatientClick = (patient) => {
        setError(''); // Clear any previous errors
        if (editingPatient?.display_id === patient.display_id) {
            // Toggle close
            setEditingPatient(null);
            setIsAddMode(false);
        } else {
            setEditingPatient(patient);
            setIsAddMode(false);
            setFormData({
                ...patient,
                patient_phone_number: '' // hidden or not needed for update
            });
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(''); // Clear previous errors

        // Sanitize gender just in case legacy state is present
        let cleanData = { ...formData };
        if (cleanData.gender === 'Male') cleanData.gender = 'M';
        if (cleanData.gender === 'Female') cleanData.gender = 'F';

        // Concatenate country code with phone number for new patients
        if (isAddMode && cleanData.patient_phone_number) {
            cleanData.patient_phone_number = countryCode + cleanData.patient_phone_number;
        }

        try {
            if (isAddMode) {
                await createPatient(cleanData);
            } else if (editingPatient) {
                await updatePatient({
                    patient_display_id: editingPatient.display_id,
                    ...cleanData
                });
            }
            await loadPatients();
            resetForm();
        } catch (err) {
            console.error(err);
            // Extract error message from response if available
            const errorMessage = err.response?.data?.error || 'Operation failed. Please check your inputs.';
            setError(errorMessage);
        }
    };

    return (
        <div className="dashboard-container">
            <header>
                <h1>Doctor Dashboard</h1>
                <div>
                    <button className="btn btn-primary" onClick={handleAddClick}>+ Add New Patient</button>
                    <button className="btn btn-secondary" onClick={handleLogout}>Logout</button>
                </div>
            </header>

            <div className="content-area">
                <div className="patient-list">
                    <h3>My Patients</h3>
                    {patients.map(p => (
                        <div key={p.display_id} className="patient-item">
                            <div className="patient-summary" onClick={() => handlePatientClick(p)}>
                                <span>{p.alias} ({p.gender}, {p.age})</span>
                                <span className="arrow">{editingPatient?.display_id === p.display_id ? '▲' : '▼'}</span>
                            </div>
                            {editingPatient?.display_id === p.display_id && (
                                <div className="patient-details-form">
                                    {error && <p className="error">{error}</p>}
                                    <PatientForm
                                        formData={formData}
                                        onChange={handleInputChange}
                                        onSubmit={handleSubmit}
                                        mode="edit"
                                        countryCode={countryCode}
                                        setCountryCode={setCountryCode}
                                    />
                                </div>
                            )}
                        </div>
                    ))}
                </div>

                {isAddMode && (
                    <div className="add-patient-panel">
                        <h3>Add New Patient</h3>
                        {error && <p className="error">{error}</p>}
                        <PatientForm
                            formData={formData}
                            onChange={handleInputChange}
                            onSubmit={handleSubmit}
                            mode="add"
                            countryCode={countryCode}
                            setCountryCode={setCountryCode}
                        />
                        <button className="btn btn-text" onClick={resetForm}>Cancel</button>
                    </div>
                )}
            </div>
        </div>
    );
};

const PatientForm = ({ formData, onChange, onSubmit, mode, countryCode, setCountryCode }) => {
    return (
        <form onSubmit={onSubmit} className="patient-form-grid">
            {mode === 'add' && (
                <div className="form-group full-width">
                    <label>Phone Number *</label>
                    <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-end', marginTop: '5px' }}>
                        <CountryCodeSelect
                            value={countryCode}
                            onChange={setCountryCode}
                        />
                        <input
                            name="patient_phone_number"
                            type="tel"
                            value={formData.patient_phone_number}
                            onChange={onChange}
                            required
                            placeholder="Phone Number"
                            style={{ flex: 1, marginTop: 0 }}
                        />
                    </div>
                </div>
            )}

            <div className="form-row">
                <div className="form-group">
                    <label>Alias *</label>
                    <input name="alias" value={formData.alias} onChange={onChange} required placeholder="Alias" />
                </div>
                <div className="form-group">
                    <label>Age *</label>
                    <input name="age" type="number" value={formData.age} onChange={onChange} required placeholder="Age" />
                </div>
            </div>

            <div className="form-row">
                <div className="form-group">
                    <label>Gender *</label>
                    <select name="gender" value={formData.gender} onChange={onChange} required>
                        <option value="">Select Gender</option>
                        <option value="M">Male</option>
                        <option value="F">Female</option>
                    </select>
                </div>
                <div className="form-group">
                    <label>Occupation</label>
                    <input name="occupation" value={formData.occupation} onChange={onChange} placeholder="Occupation" />
                </div>
            </div>

            <div className="form-row">
                <div className="form-group">
                    <label>Married</label>
                    <select name="married" value={formData.married} onChange={onChange}>
                        <option value="false">No</option>
                        <option value="true">Yes</option>
                    </select>
                </div>
                <div className="form-group">
                    <label>Smoker</label>
                    <select name="smoke" value={formData.smoke} onChange={onChange}>
                        <option value="false">No</option>
                        <option value="true">Yes</option>
                    </select>
                </div>
            </div>

            <div className="form-group full-width">
                <label>Weekly Sport (hrs)</label>
                <input name="weekly_sport_activity" value={formData.weekly_sport_activity} onChange={onChange} placeholder="Weekly Sport Activity" />
            </div>

            <div className="form-group full-width">
                <label>Diagnostic</label>
                <input name="mental_illness_diagnostic" value={formData.mental_illness_diagnostic} onChange={onChange} placeholder="Diagnostic" />
            </div>

            <div className="form-group full-width">
                <label>Medications</label>
                <input name="medications" value={formData.medications} onChange={onChange} placeholder="Medications" />
            </div>

            <button type="submit" className="btn btn-success full-width">{mode === 'add' ? 'Create Patient' : 'Update Details'}</button>
        </form>
    );
};

export default Dashboard;
