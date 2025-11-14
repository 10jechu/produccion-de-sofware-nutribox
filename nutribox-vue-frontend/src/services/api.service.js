import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Crear instancia de axios con configuración global
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // Aumentado a 30 segundos
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// INTERCEPTOR para agregar token automáticamente a TODAS las peticiones
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('nutribox_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    console.log('🔄 Enviando petición:', config.method?.toUpperCase(), config.url);
    console.log('🔑 Token incluido:', !!token);
    return config;
  },
  (error) => {
    console.error('❌ Error en interceptor de request:', error);
    return Promise.reject(error);
  }
);

// INTERCEPTOR para manejar errores - CORREGIDO
apiClient.interceptors.response.use(
  (response) => {
    console.log('✅ Respuesta exitosa:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('❌ Error en petición:', error.response?.status, error.config?.url);
    console.error('📋 Detalles del error:', error.response?.data);
    
    // Manejar error 401 (No autorizado)
    if (error.response?.status === 401) {
      console.warn('⚠️ Token inválido o expirado, cerrando sesión...');
      localStorage.removeItem('nutribox_token');
      localStorage.removeItem('nutribox_user');
      
      // Solo redirigir si no estamos en login
      if (!window.location.href.includes('/login')) {
        window.location.href = '/login';
      }
    }
    
    // Manejar error 500 (Error del servidor)
    if (error.response?.status === 500) {
      console.error('🔥 Error interno del servidor');
    }
    
    return Promise.reject(error);
  }
);

const apiService = {
  async request(method, endpoint, data = null, customHeaders = {}) {
    try {
      const config = {
        method,
        url: endpoint,
        headers: {
          ...customHeaders,
        },
      };

      if (data) {
        if (method === 'get') {
          config.params = data;
        } else {
          config.data = data;
        }
      }

      console.log(`📤 ${method.toUpperCase()} ${endpoint}`, data || '');
      const response = await apiClient.request(config);
      return response.data;
      
    } catch (error) {
      console.error(`❌ Error en ${method.toUpperCase()} ${endpoint}:`, error);
      
      // Propagar el error para manejo específico en componentes
      if (error.response?.status === 401) {
        throw new Error('No autorizado. Por favor, inicie sesión nuevamente.');
      } else if (error.response?.status === 404) {
        throw new Error('Recurso no encontrado.');
      } else if (error.response?.data?.message) {
        throw new Error(error.response.data.message);
      } else {
        throw new Error(error.message || 'Error de conexión');
      }
    }
  },

  get(endpoint, params = {}) {
    return this.request('get', endpoint, params);
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

// En api.service.js, agregar después de put():
patch(endpoint, data) {
  return this.request('patch', endpoint, data);
},

  delete(endpoint) {
    return this.request('delete', endpoint);
  },
};

export default apiService;