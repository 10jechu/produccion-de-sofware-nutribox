// src/services/auth.service.js
import apiService from './api.service'; // Importa el servicio API

const authService = {
  async login(email, password) {
    const endpoint = '/auth/login'; // Endpoint relativo
    // FastAPI espera datos de formulario para OAuth2PasswordRequestForm
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
      const response = await apiService.postLogin(endpoint, formData);
      if (response.access_token) {
        this.saveToken(response.access_token);
        // Podrías obtener y guardar datos del usuario aquí si es necesario
        // await this.fetchAndSaveUser(email); // Ejemplo
      }
      return response; // Devuelve la respuesta completa (incluye token)
    } catch (error) {
      console.error('Error en login:', error);
      this.removeToken(); // Limpia token en caso de error
      throw error; // Re-lanza el error para que el componente lo maneje
    }
  },

  async register(userData) {
    const endpoint = '/auth/register';
    try {
        // Asume que la API espera un JSON para el registro
        const response = await apiService.post(endpoint, {
            nombre: userData.nombre,
            email: userData.email,
            password: userData.password,
            membresia: userData.membresia,
            rol: 'Usuario' // Rol fijo según tu backend
        });
        return response; // Devuelve la respuesta del backend (ej. {id, email})
    } catch (error) {
        console.error('Error en registro:', error);
        throw error;
    }
  },

  saveToken(token) {
    localStorage.setItem('nutribox_token', token);
  },

  getToken() {
    return localStorage.getItem('nutribox_token');
  },

  removeToken() {
    localStorage.removeItem('nutribox_token');
    // Limpiar también datos de usuario si los guardas
    // localStorage.removeItem('nutribox_user');
  },

  isAuthenticated() {
    return !!this.getToken();
  },

  logout() {
    this.removeToken();
    // La redirección se manejará en el componente o en el router guard
  },

  // --- Funciones para guardar/obtener usuario (ejemplo) ---
  /*
  async fetchAndSaveUser(email) {
      // Necesitarías un endpoint en tu backend para obtener datos del usuario por email o ID
      // Ejemplo: const user = await apiService.get('/users/me'); // O buscar por email
      // if (user) {
      //   this.saveUser(user);
      // }
  },
  saveUser(user) {
      localStorage.setItem('nutribox_user', JSON.stringify(user));
  },
  getUser() {
      const user = localStorage.getItem('nutribox_user');
      return user ? JSON.parse(user) : null;
  }
  */
};

export default authService;