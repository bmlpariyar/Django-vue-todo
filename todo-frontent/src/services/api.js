// src/services/api.js

import axios from 'axios';
import authService from './auth';

const API_URL = 'http://127.0.0.1:8000'; // Replace with your actual API URL

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = authService.getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshed = await authService.refreshToken();
        if (refreshed) {
          return api(originalRequest);
        }
      } catch (refreshError) {
        authService.logout();
      }
    }
    return Promise.reject(error);
  }
);

export default api;