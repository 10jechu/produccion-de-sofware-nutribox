// Función genérica de fetch
const apiFetch = async (endpoint, options = {}) => {
    // ASEGURA QUE EL ENDPOINT SIEMPRE TENGA UN SLASH FINAL para evitar redirecciones 307
    if (endpoint.length > 1 && !endpoint.endsWith('/')) {
        endpoint = endpoint + '/';
    }

    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token && !options.skipAuth) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const config = {
        ...options,
        headers
    };
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}${endpoint}`, config);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error en la petición');
        }
        
        if (response.status === 204) {
            return {}; 
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
};

// AUTH
const API = {
    // Autenticación
    register: (data) => {
        return apiFetch('/auth/register', {
            method: 'POST',
            body: JSON.stringify(data),
            skipAuth: true
        });
    },
    
    login: async (email, password) => {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        
        const response = await fetch(`${CONFIG.API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Credenciales inválidas');
        }
        
        return await response.json();
    },
    
    // Usuarios
    getUsers: () => apiFetch('/users'),
    getUserDetail: (id) => apiFetch(`/users/${id}/detail`),
    updateUser: (id, data) => apiFetch(`/users/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data)
    }),
    
    // Hijos
    getChildren: (usuarioId) => apiFetch(`/children?usuario_id=${usuarioId}`),
    getChildDetail: (id) => apiFetch(`/children/${id}/detail`),
    createChild: (data) => apiFetch('/children', {
        method: 'POST',
        body: JSON.stringify(data)
    }),
    updateChild: (id, data) => apiFetch(`/children/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data)
    }),
    deleteChild: (id) => apiFetch(`/children/${id}`, {
        method: 'DELETE'
    }),
    
    // Direcciones
    getAddresses: (usuarioId) => apiFetch(`/addresses?usuario_id=${usuarioId}`),
    createAddress: (data) => apiFetch('/addresses', {
        method: 'POST',
        body: JSON.stringify(data)
    }),
    updateAddress: (id, data) => apiFetch(`/addresses/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data)
    }),
    deleteAddress: (id) => apiFetch(`/addresses/${id}`, {
        method: 'DELETE'
    }),
    
    // Alimentos
    getFoods: (onlyActive = 'true') => apiFetch(`/foods?only_active=${onlyActive}`),
    getFood: (id) => apiFetch(`/foods/${id}`),
    
    // Loncheras
    getLunchboxes: (hijoId = null) => {
        const query = hijoId ? `?hijo_id=${hijoId}` : '';
        return apiFetch(`/lunchboxes${query}`);
    },
    getLunchboxDetail: (id) => apiFetch(`/lunchboxes/${id}/detail`),
    createLunchbox: (data) => apiFetch('/lunchboxes', {
        method: 'POST',
        body: JSON.stringify(data)
    }),
    updateLunchbox: (id, data) => apiFetch(`/lunchboxes/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data)
    }),
    addItemToLunchbox: (lunchboxId, data) => apiFetch(`/lunchboxes/${lunchboxId}/items`, {
        method: 'POST',
        body: JSON.stringify(data)
    }),
    updateLunchboxItem: (lunchboxId, alimentoId, data) => apiFetch(`/lunchboxes/${lunchboxId}/items/${alimentoId}`, {
        method: 'PATCH',
        body: JSON.stringify(data)
    }),
    removeItemFromLunchbox: (lunchboxId, alimentoId) => apiFetch(`/lunchboxes/${lunchboxId}/items/${alimentoId}`, {
        method: 'DELETE'
    }),
    
    // Restricciones
    getRestrictions: (hijoId) => apiFetch(`/restrictions?hijo_id=${hijoId}`),
    createRestriction: (data) => apiFetch('/restrictions', {
        method: 'POST',
        body: JSON.stringify(data)
    }),
    deleteRestriction: (id) => apiFetch(`/restrictions/${id}`, {
        method: 'DELETE'
    })
};
