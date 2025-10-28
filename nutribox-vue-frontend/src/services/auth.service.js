// src/services/auth.service.js
import apiService from './api.service';
import { getUserDetail } from '@/utils/user'; 

const authService = {
  // Función auxiliar CORREGIDA: Usa el nuevo endpoint por email y concatenación
  async fetchAndSaveUserDetail(email) {
      // CORRECCIÓN FINAL: Concatenación simple para evitar corrupción de caracteres
      const detailedUser = await apiService.get('/users/by-email/' + email + '/detail');

      this.saveUserDetail(detailedUser);
      return detailedUser;
  },

  async login(email, password) {
    const endpoint = '/auth/login';
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
      const response = await apiService.postLogin(endpoint, formData);
      if (response.access_token) {
        this.saveToken(response.access_token);
        await this.fetchAndSaveUserDetail(email);
      }
      return response; 
    } catch (error) {
      console.error('Error en login:', error);
      this.removeToken(); 
      this.removeUserDetail(); 
      throw error;
    }
  },

  async register(userData) {
    const endpoint = '/auth/register';
    try {
        const response = await apiService.post(endpoint, {
            nombre: userData.nombre,
            email: userData.email,
            password: userData.password,
            membresia: userData.membresia,
            rol: 'Usuario'
        });
        return response;
    } catch (error) {
        console.error('Error en registro:', error);
        throw error;
    }
  },

  saveToken(token) {
    localStorage.setItem('nutribox_token', token);
  },

  removeToken() {
    localStorage.removeItem('nutribox_token');
  },
  
  saveUserDetail(user) {
      localStorage.setItem('nutribox_user', JSON.stringify(user));
  },
  
  removeUserDetail() {
      localStorage.removeItem('nutribox_user');
  },

  isAuthenticated() {
    return !!this.getToken() && !!getUserDetail();
  },

  logout() {
    this.removeToken();
    this.removeUserDetail();
  },

  getToken() {
    return localStorage.getItem('nutribox_token');
  }
};

export default authService;
