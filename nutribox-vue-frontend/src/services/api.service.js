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

// INTERCEPTOR para manejar errores - MODIFICADO
apiClient.interceptors.response.use(
  (response) => {
    console.log('✅ Response success:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('❌ Response error:', {
      status: error.response?.status,
      url: error.config?.url,
      method: error.config?.method,
      data: error.response?.data
    });
    
    // ✅ MODIFICADO: No cerrar sesión automáticamente
    if (error.response?.status === 401) {
      console.warn('🔐 401 Unauthorized - Pero NO cerramos sesión');
      // Solo mostrar alerta, no redirigir
      // localStorage.removeItem('nutribox_token');
      // localStorage.removeItem('nutribox_user');
      // window.location.href = '/login';
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