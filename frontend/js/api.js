// Función genérica de fetch
const apiFetch = async (endpoint, options = {}) => {
    // ASEGURA QUE EL ENDPOINT TENGA UN SLASH FINAL SOLO SI NO TIENE QUERY PARAMS
    if (endpoint.length > 1 && !endpoint.endsWith('/') && !endpoint.includes('?')) {
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
            // Intenta obtener el detalle del error, si no, usa el texto de estado
            let errorDetail = 'Error en la petición';
            try {
                const error = await response.json();
                errorDetail = error.detail || JSON.stringify(error);
            } catch (jsonError) {
                errorDetail = response.statusText;
            }
            throw new Error(errorDetail);
        }

        if (response.status === 204) { // No Content
            return {};
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        // Re-lanza el error para que sea capturado por quien llamó a apiFetch
        throw error;
    }
};

// API
const API = {
    // Autenticación
    register: (data) => {
        return apiFetch('/auth/register', {
            method: 'POST',
            body: JSON.stringify(data),
            skipAuth: true // No se necesita token para registrarse
        });
    },

    login: async (email, password) => {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        // Usamos fetch directamente aquí porque requiere 'application/x-www-form-urlencoded'
        const response = await fetch(`${CONFIG.API_BASE_URL}/auth/login/`, { // Asegúrate que el endpoint de login termine en / si es necesario
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });

        if (!response.ok) {
            // Intenta obtener el detalle del error, si no, usa un mensaje genérico
            let errorDetail = 'Credenciales inválidas';
             try {
                const error = await response.json();
                errorDetail = error.detail || errorDetail;
            } catch (jsonError) {
                 // Si no hay JSON, usa el statusText
                 errorDetail = response.statusText || errorDetail;
            }
            throw new Error(errorDetail);
        }

        return await response.json();
    },

    // Usuarios
    getUsers: () => apiFetch('/users'), // Nota: Sin / al final aquí, apiFetch lo añade si es necesario
    getUserDetail: (id) => apiFetch(`/users/${id}/detail`),
    updateUser: (id, data) => apiFetch(`/users/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data)
    }),

    // Hijos
    getChildren: (usuarioId) => apiFetch(`/children?usuario_id=${usuarioId}`), // Ya tiene '?', apiFetch no añade /
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
    getAddresses: (usuarioId) => apiFetch(`/addresses?usuario_id=${usuarioId}`), // Ya tiene '?'
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
    createFood: (data) => apiFetch('/foods', {
        method: 'POST',
        body: JSON.stringify(data)
    }),
    getFoods: (onlyActive = 'true') => apiFetch(`/foods?only_active=${onlyActive}`),
    getFood: (id) => apiFetch(`/foods/${id}`),
    // ===== FUNCIONES NUEVAS AQUÍ =====
    updateFood: (id, data) => apiFetch(`/foods/${id}`, { // PATCH para actualizar
        method: 'PATCH',
        body: JSON.stringify(data)
    }),
    deleteFood: (id) => apiFetch(`/foods/${id}`, { // DELETE (el backend hace soft delete)
        method: 'DELETE'
    }),

    // Loncheras
    getLunchboxes: (hijoId = null) => {
        const query = hijoId ? `?hijo_id=${hijoId}` : '';
        // Si hay query, no se añade /, si no hay query, apiFetch lo añade
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
    // ----- FUNCIONES QUE FALTABAN -----
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

    deleteLunchbox: (id) => apiFetch(`/lunchboxes/${id}`, {
        method: 'DELETE'
    }),
    // ------------------------------------

    // Restricciones
    getRestrictions: (hijoId) => apiFetch(`/restrictions?hijo_id=${hijoId}`),
    createRestriction: (data) => apiFetch('/restrictions', {
        method: 'POST',
        body: JSON.stringify(data)
    }),
    deleteRestriction: (id) => apiFetch(`/restrictions/${id}`, {
        method: 'DELETE'
    })
}; // <--- ESTA ES LA PARTE CRÍTICA QUE DEBE ESTAR AL FINAL Y CORRECTA