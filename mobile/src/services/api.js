import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_URL = process.env.API_URL || 'http://192.168.1.100:5000';

const api = axios.create({
  baseURL: API_URL,
  timeout: parseInt(process.env.API_TIMEOUT || '30000'),
});

// Add token to requests
api.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle responses
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      await AsyncStorage.removeItem('authToken');
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (email, password) => api.post('/api/auth/login', { email, password }),
  register: (email, password, name) => api.post('/api/auth/register', { email, password, name }),
  logout: () => api.post('/api/auth/logout'),
};

export const vehiclesAPI = {
  list: () => api.get('/api/vehicles'),
  get: (id) => api.get(`/api/vehicles/${id}`),
  create: (data) => api.post('/api/vehicles', data),
  update: (id, data) => api.put(`/api/vehicles/${id}`, data),
  delete: (id) => api.delete(`/api/vehicles/${id}`),
};

export const tripsAPI = {
  list: () => api.get('/api/trips'),
  get: (id) => api.get(`/api/trips/${id}`),
  start: (vehicleId) => api.post('/api/trips', { vehicleId }),
  end: (id) => api.post(`/api/trips/${id}/end`),
  getRoute: (id) => api.get(`/api/trips/${id}/route`),
};

export const gpsAPI = {
  update: (data) => api.post('/api/gps/update', data),
};

export default api;
