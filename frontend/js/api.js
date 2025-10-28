const apiFetch = async (endpoint, options = {}) => {
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
        
        // ⬇️ AGREGAR ESTO: Manejar respuestas sin contenido (204 No Content)
        if (response.status === 204 || response.headers.get('content-length') === '0') {
            return null;
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
};