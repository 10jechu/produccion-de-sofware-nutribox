// src/services/api.service.js

// Obtener la URL base de las variables de entorno de Vite
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1'; // URL por defecto si no esta definida

// Funcion auxiliar para obtener Headers
const getHeaders = (isFormData = false) => {
  const headers = {};
  if (!isFormData) {
    headers['Content-Type'] = 'application/json';
  }
  const token = localStorage.getItem('nutribox_token');
  if (token) {
    // Usamos concatenacion simple para la autorizacion
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
  // Si la respuesta es 204 No Content, devuelve un objeto vacio
  if (response.status === 204) {
    return {};
  }
  return response.json();
};

// Funcion auxiliar para asegurar que el endpoint NO tenga prefijos de idioma corruptos
const prepareEndpoint = (endpoint) => {
    // Asegura que no haya prefijos de idioma como /v_en/ o /v_es/ en la URL
    let finalEndpoint = endpoint.replace(/v_(en|es)\//g, ''); 
    
    const startsWithSlash = finalEndpoint.startsWith('/');
    const endsWithSlash = finalEndpoint.endsWith('/');
    
    // Garantizar el slash inicial
    finalEndpoint = startsWithSlash ? finalEndpoint : '/' + finalEndpoint;
    
    // Garantizar el slash final si no hay query params y no termina en slash
    if (finalEndpoint.length > 1 && !endsWithSlash && !finalEndpoint.includes('?')) {
        finalEndpoint = finalEndpoint + '/';
    }
    
    return finalEndpoint;
}

// Servicio API
const apiService = {
  get: async (endpoint, params = null) => {
    const finalEndpoint = prepareEndpoint(endpoint);
    let url = API_BASE_URL + finalEndpoint; // CONCATENACION
    if (params) {
      url += '?' + (new URLSearchParams(params).toString()); // CONCATENACION
    }
    const response = await fetch(url, {
      method: 'GET',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },

  post: async (endpoint, body) => {
    const finalEndpoint = prepareEndpoint(endpoint);
    const response = await fetch(API_BASE_URL + finalEndpoint, { // CONCATENACION
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(body),
    });
    return handleResponse(response);
  },

  postLogin: async (endpoint, formDataParams) => {
    const finalEndpoint = prepareEndpoint(endpoint);
    const response = await fetch(API_BASE_URL + finalEndpoint, { // CONCATENACION
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formDataParams,
    });
    return handleResponse(response);
  },

  patch: async (endpoint, body) => {
    const finalEndpoint = prepareEndpoint(endpoint);
    const response = await fetch(API_BASE_URL + finalEndpoint, { // CONCATENACION
      method: 'PATCH',
      headers: getHeaders(),
      body: JSON.stringify(body),
    });
    return handleResponse(response);
  },

  delete: async (endpoint) => {
    const finalEndpoint = prepareEndpoint(endpoint);
    const response = await fetch(API_BASE_URL + finalEndpoint, { // CONCATENACION
      method: 'DELETE',
      headers: getHeaders(),
    });
    return handleResponse(response);
  },
};

export default apiService;