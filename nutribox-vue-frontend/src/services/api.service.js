// src/services/api.service.js

// Obtener la URL base de las variables de entorno de Vite
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

// Funcion auxiliar para obtener Headers
const getHeaders = (isFormData = false) => {
  const headers = {};
  if (!isFormData) {
    headers['Content-Type'] = 'application/json';
  }
  const token = localStorage.getItem('nutribox_token');
  if (token) {
    headers['Authorization'] = 'Bearer ' + token;
  }
  return headers;
};

// Funcion auxiliar para manejar respuestas
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(errorData.detail || 'Error en la peticion');
  }
  if (response.status === 204) {
    return {};
  }
  return response.json();
};

// --- ELIMINADA LA FUNCION 'prepareEndpoint' ---

// Servicio API
const apiService = {
  get: async (endpoint, params = null) => {
    // CORREGIDO: No se usa prepareEndpoint
    let url = API_BASE_URL + endpoint; 
    if (params) {
      url += '?' + (new URLSearchParams(params).toString());
    }
    const response = await fetch(url, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  post: async (endpoint, body) => {
    // CORREGIDO: No se usa prepareEndpoint
    const response = await fetch(API_BASE_URL + endpoint, { 
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(body),
    });
    return handleResponse(response);
  },

  postLogin: async (endpoint, formDataParams) => {
    // CORREGIDO: No se usa prepareEndpoint
    const response = await fetch(API_BASE_URL + endpoint, { 
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formDataParams,
    });
    return handleResponse(response);
  },

  patch: async (endpoint, body) => {
    // CORREGIDO: No se usa prepareEndpoint
    const response = await fetch(API_BASE_URL + endpoint, { 
      method: 'PATCH',
      headers: getHeaders(),
      body: JSON.stringify(body),
    });
    return handleResponse(response);
  },

  delete: async (endpoint) => {
    // CORREGIDO: No se usa prepareEndpoint
    const response = await fetch(API_BASE_URL + endpoint, { 
      method: 'DELETE',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },
};

export default apiService;
