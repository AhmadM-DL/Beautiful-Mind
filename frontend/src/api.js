
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user_role');
            localStorage.removeItem('username');
            if (window.location.pathname !== '/') {
                window.location.href = '/';
            }
        }
        return Promise.reject(error);
    }
);

export const login = async (identifier, password) => {
    const response = await api.post('/login', { identifier, password });
    if (response.data.token) {
        localStorage.setItem('access_token', response.data.token);
        localStorage.setItem('user_role', response.data.role);
        localStorage.setItem('username', response.data.user);
    }
    return response.data;
};

export const registerDoctor = async (data) => {
    const response = await api.post('/doctor/register', data);
    return response.data;
};

export const getPatients = async () => {
    const response = await api.get('/doctor/patients');
    return response.data;
};

export const createPatient = async (data) => {
    const response = await api.post('/doctor/patient', data);
    return response.data;
};

export const updatePatient = async (data) => {
    // Expects data to contain patient_display_id and fields to update
    const response = await api.put('/doctor/patient', data);
    return response.data;
};

export default api;
