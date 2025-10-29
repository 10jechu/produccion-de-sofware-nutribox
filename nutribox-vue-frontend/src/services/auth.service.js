// src/services/auth.service.js
import apiService from './api.service';
import { getUserDetail } from '@/utils/user';

const authService = {
  // Función auxiliar AJUSTADA: Recibe userId, llama al endpoint correcto.
  async fetchAndSaveUserDetail(userId) { // Cambiado 'email' por 'userId'
    try {
      // Llama al endpoint correcto usando el ID del usuario
      // Se usa concatenación simple para la URL
      const detailedUser = await apiService.get('/users/' + userId + '/detail');

      this.saveUserDetail(detailedUser); // Guarda el objeto completo del usuario en localStorage
      console.log("User detail saved:", detailedUser); // Log para confirmar
      return detailedUser;
    } catch (error) {
      console.error("Error fetching user detail by ID:", error);
      // Si falla obtener los detalles, es mejor desloguear para evitar inconsistencias
      this.logout();
      throw new Error("No se pudieron cargar los detalles completos del usuario.");
    }
  },

  async login(email, password) {
    const endpoint = '/auth/login';
    const formData = new URLSearchParams();
    formData.append('username', email); // FastAPI usa 'username' por defecto para OAuth2PasswordRequestForm
    formData.append('password', password);

    try {
      // 1. Intenta hacer login y obtener el token
      const response = await apiService.postLogin(endpoint, formData);

      if (response.access_token) {
        this.saveToken(response.access_token); // Guarda el token

        // 2. OBTENER EL USER ID DESPUÉS DEL LOGIN EXITOSO
        //    Opción A (Recomendada si puedes modificar el backend):
        //    Modifica el endpoint /auth/login para que devuelva también el user.id
        //    const userId = response.user_id; // Suponiendo que el backend lo devuelve

        //    Opción B (Alternativa si no puedes modificar el backend):
        //    Busca el ID haciendo un GET a /users y filtrando por email
        //    Nota: Esto puede ser ineficiente si hay muchos usuarios.
        console.log("Login successful, fetching user list to find ID for:", email);
        const users = await apiService.get('/users'); // Llama a listar usuarios
        const currentUser = users.find(u => u.email === email); // Encuentra el usuario por email
        if (!currentUser) {
          console.error("User not found in list after successful login:", email);
          throw new Error("Usuario no encontrado después del login.");
        }
        const userId = currentUser.id; // Obtiene el ID
        console.log("User ID found:", userId);

        // 3. Obtener y guardar los detalles completos del usuario usando el ID
        await this.fetchAndSaveUserDetail(userId);

      } else {
         // Si el login no devuelve token (aunque la petición sea 200 OK), es un error
         throw new Error("Respuesta de login inválida, no se recibió token.");
      }
      return response; // Devuelve la respuesta original del login (que contiene el token)
    } catch (error) {
      console.error('Error en el proceso de login:', error);
      // Limpia cualquier credencial parcial guardada si el proceso falla
      this.removeToken();
      this.removeUserDetail();
      throw error; // Re-lanza el error para que LoginView.vue lo capture y muestre
    }
  },

  async register(userData) {
    const endpoint = '/auth/register';
    try {
      // Asegúrate que los nombres de campo coincidan con UserRegister en el backend
      const response = await apiService.post(endpoint, {
        nombre: userData.nombre,
        email: userData.email,
        password: userData.password,
        membresia: userData.membresia, // 'Free', 'Estandar', 'Premium'
        rol: 'Usuario' // Rol fijo
      });
      return response;
    } catch (error) {
      console.error('Error en registro:', error);
      throw error; // Re-lanza para que RegisterView.vue lo maneje
    }
  },

  saveToken(token) {
    localStorage.setItem('nutribox_token', token);
  },

  removeToken() {
    localStorage.removeItem('nutribox_token');
  },

  saveUserDetail(user) {
    // Guarda el objeto de usuario completo (incluyendo rol, membresía, etc.)
    localStorage.setItem('nutribox_user', JSON.stringify(user));
  },

  removeUserDetail() {
    localStorage.removeItem('nutribox_user');
  },

  // Verifica si hay token Y datos de usuario guardados
  isAuthenticated() {
    return !!this.getToken() && !!getUserDetail();
  },

  logout() {
    this.removeToken();
    this.removeUserDetail();
    // Podrías añadir una redirección aquí si fuera necesario,
    // pero usualmente se maneja en el componente/vista que llama a logout.
  },

  getToken() {
    return localStorage.getItem('nutribox_token');
  }
};

export default authService;
