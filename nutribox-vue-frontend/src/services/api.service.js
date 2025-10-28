// src/services/api.service.js

// Obtener la URL base de las variables de entorno de Vite
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1'; // URL por defecto si no está definida

// Función auxiliar para obtener Headers
const getHeaders = (isFormData = false) => {
  const headers = {};
  if (!isFormData) {
    headers['Content-Type'] = 'application/json';
  }
  const token = localStorage.getItem('nutribox_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

// Función auxiliar para manejar respuestas
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(errorData.detail || 'Error en la petición');
  }
  // Si la respuesta es 204 No Content, devuelve un objeto vacío
  if (response.status === 204) {
    return {};
  }
  return response.json();
};

// Función auxiliar para asegurar que el endpoint termine en /
const prepareEndpoint = (endpoint) => {
    const startsWithSlash = endpoint.startsWith('/');
    const endsWithSlash = endpoint.endsWith('/');
    let finalEndpoint = startsWithSlash ? endpoint : `/${endpoint}`;
    if (finalEndpoint.length > 1 && !endsWithSlash) {
        finalEndpoint = `${finalEndpoint}/`;
    }
    return finalEndpoint;
}

// Servicio API
const apiService = {
  get: async (endpoint, params = null) => {
    const finalEndpoint = prepareEndpoint(endpoint);
    let url = `${API_BASE_URL}${finalEndpoint}`;
    if (params) {
      url += `?${new URLSearchParams(params).toString()}`;
    }
    const response = await fetch(url, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  post: async (endpoint, body) => {
    const finalEndpoint = prepareEndpoint(endpoint);
    const response = await fetch(`${API_BASE_URL}${finalEndpoint}`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(body),
    });
    return handleResponse(response);
  },

  // Específico para login (x-www-form-urlencoded)
  postLogin: async (endpoint, formDataParams) => {
    const finalEndpoint = prepareEndpoint(endpoint);
    const response = await fetch(`${API_BASE_URL}${finalEndpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        // No incluimos token aquí usualmente para login
      },
      body: formDataParams, // formDataParams ya debe ser un URLSearchParams
    });
    return handleResponse(response);
  },

  patch: async (endpoint, body) => {
    const finalEndpoint = prepareEndpoint(endpoint);
    const response = await fetch(`${API_BASE_URL}${finalEndpoint}`, {
      method: 'PATCH',
      headers: getHeaders(),
      body: JSON.stringify(body),
    });
    return handleResponse(response);
  },

  delete: async (endpoint) => {
    const finalEndpoint = prepareEndpoint(endpoint);
    const response = await fetch(`${API_BASE_URL}${finalEndpoint}`, {
      method: 'DELETE',
      headers: getHeaders(),
    });
    return handleResponse(response); // Manejará el 204 No Content
  },
};

export default apiService;