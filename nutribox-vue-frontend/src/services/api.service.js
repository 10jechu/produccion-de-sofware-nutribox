import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Crear instancia de axios con configuración global
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// INTERCEPTOR para agregar token automáticamente a TODAS las peticiones
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('nutribox_token');
    if (token) {
      config.headers.Authorization = 'Bearer ' + token;
    }
    console.log('Enviando petición:', config.method?.toUpperCase(), config.url);
    console.log('Token incluido:', !!token);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// INTERCEPTOR para manejar errores
apiClient.interceptors.response.use(
  (response) => {
    console.log('Respuesta exitosa:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('Error en petición:', error.response?.status, error.config?.url);
    console.error('Detalles:', error.response?.data);
    return Promise.reject(error);
  }
);

const apiService = {
  async request(method, endpoint, data = null, headers = {}) {
    try {
      const config = {
        method,
        url: endpoint,
        headers: {
          'Content-Type': 'application/json',
          ...headers,
        },
      };

      if (data) {
        config.data = data;
      }

      const response = await apiClient.request(config);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  get(endpoint, params = null) {
    return this.request('get', endpoint, null, params);
  },

  post(endpoint, data, headers = {}) {
    return this.request('post', endpoint, data, headers);
  },

  postLogin(endpoint, formData) {
    return this.request('post', endpoint, formData, {
      'Content-Type': 'application/x-www-form-urlencoded',
    });
  },

  put(endpoint, data) {
    return this.request('put', endpoint, data);
  },

  delete(endpoint) {
    return this.request('delete', endpoint);
  },
};

export default apiService;
