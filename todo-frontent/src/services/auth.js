// src/services/auth.js

import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000'; // Replace with your actual API URL

const authService = {
  async login(username, password) {
    const response = await axios.post(`${API_URL}/api/token/`, {
      username,
      password
    });
    if (response.data.access) {
      localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
  },

  logout() {
    localStorage.removeItem('user');
  },

  getCurrentUser() {
    return JSON.parse(localStorage.getItem('user'));
  },

  getToken() {
    const user = this.getCurrentUser();
    return user ? user.access : null;
  },

  async refreshToken() {
    const user = this.getCurrentUser();
    if (user && user.refresh) {
      const response = await axios.post(`${API_URL}/api/token/refresh/`, {
        refresh: user.refresh
      });
      if (response.data.access) {
        user.access = response.data.access;
        localStorage.setItem('user', JSON.stringify(user));
      }
      return response.data;
    }
    return null;
  }
};

export default authService;