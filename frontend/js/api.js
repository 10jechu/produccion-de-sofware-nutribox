// api.js - Helper para peticiones HTTP a la API de NutriBox

// ========================================
// CONFIGURACIÓN
// ========================================

const API_BASE_URL = 'http://localhost:8000/api/v1';

// ========================================
// CLASE API
// ========================================

class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    /**
     * Obtiene el token de autenticación del localStorage
     * @returns {string|null}
     */
    getToken() {
        return localStorage.getItem('token');
    }

    /**
     * Obtiene los headers por defecto
     * @param {boolean} includeAuth - Incluir header de autenticación
     * @returns {Object}
     */
    getHeaders(includeAuth = true) {
        const headers = {
            'Content-Type': 'application/json'
        };

        if (includeAuth) {
            const token = this.getToken();
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }
        }

        return headers;
    }

    /**
     * Maneja errores de las peticiones
     * @param {Response} response - Respuesta fetch
     */
    async handleError(response) {
        let errorData;

        try {
            errorData = await response.json();
        } catch {
            errorData = { detail: 'Error desconocido' };
        }

        const error = new Error(errorData.detail || errorData.message || 'Error en la petición');
        error.status = response.status;
        error.detail = errorData.detail;
        error.response = response;

        // Si es 401, redirigir al login
        if (response.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = 'login.html';
        }

        throw error;
    }

    /**
     * Petición GET
     * @param {string} endpoint - Endpoint de la API
     * @param {Object} options - Opciones adicionales
     * @returns {Promise<Response>}
     */
    async get(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'GET',
                headers: this.getHeaders(),
                ...options
            });

            if (!response.ok) {
                await this.handleError(response);
            }

            return response;
        } catch (error) {
            console.error('GET Error:', error);
            throw error;
        }
    }

    /**
     * Petición POST
     * @param {string} endpoint - Endpoint de la API
     * @param {Object} data - Datos a enviar
     * @param {Object} options - Opciones adicionales
     * @returns {Promise<Response>}
     */
    async post(endpoint, data, options = {}) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(data),
                ...options
            });

            if (!response.ok) {
                await this.handleError(response);
            }

            return response;
        } catch (error) {
            console.error('POST Error:', error);
            throw error;
        }
    }

    /**
     * Petición PATCH
     * @param {string} endpoint - Endpoint de la API
     * @param {Object} data - Datos a actualizar
     * @param {Object} options - Opciones adicionales
     * @returns {Promise<Response>}
     */
    async patch(endpoint, data, options = {}) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'PATCH',
                headers: this.getHeaders(),
                body: JSON.stringify(data),
                ...options
            });

            if (!response.ok) {
                await this.handleError(response);
            }

            return response;
        } catch (error) {
            console.error('PATCH Error:', error);
            throw error;
        }
    }

    /**
     * Petición DELETE
     * @param {string} endpoint - Endpoint de la API
     * @param {Object} options - Opciones adicionales
     * @returns {Promise<Response>}
     */
    async delete(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'DELETE',
                headers: this.getHeaders(),
                ...options
            });

            if (!response.ok && response.status !== 204) {
                await this.handleError(response);
            }

            return response;
        } catch (error) {
            console.error('DELETE Error:', error);
            throw error;
        }
    }

    // ========================================
    // MÉTODOS DE AUTENTICACIÓN
    // ========================================

    /**
     * Login de usuario
     * @param {string} email - Email del usuario
     * @param {string} password - Contraseña
     * @returns {Promise<Object>} Token y datos del usuario
     */
    async login(email, password) {
        try {
            // FastAPI OAuth2 usa form data para login
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            const response = await fetch(`${this.baseURL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData
            });

            if (!response.ok) {
                await this.handleError(response);
            }

            const data = await response.json();

            // Guardar token
            localStorage.setItem('token', data.access_token);

            // Obtener datos del usuario
            const userResponse = await this.get('/users/me');
            const user = await userResponse.json();

            // Guardar usuario
            localStorage.setItem('user', JSON.stringify(user));

            return { token: data.access_token, user };

        } catch (error) {
            console.error('Login Error:', error);
            throw error;
        }
    }

    /**
     * Registro de usuario
     * @param {Object} userData - Datos del usuario
     * @returns {Promise<Object>}
     */
    async register(userData) {
        try {
            const response = await fetch(`${this.baseURL}/auth/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            if (!response.ok) {
                await this.handleError(response);
            }

            return await response.json();

        } catch (error) {
            console.error('Register Error:', error);
            throw error;
        }
    }

    /**
     * Logout
     */
    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = 'login.html';
    }

    // ========================================
    // MÉTODOS ESPECÍFICOS DE RESTRICCIONES
    // ========================================

    /**
     * Obtiene restricciones de un hijo
     * @param {number} hijoId - ID del hijo
     * @returns {Promise<Array>}
     */
    async getRestrictions(hijoId) {
        const response = await this.get(`/restrictions?hijo_id=${hijoId}`);
        return await response.json();
    }

    /**
     * Valida restricciones de una lonchera
     * @param {number} lunchboxId - ID de la lonchera
     * @returns {Promise<Object>}
     */
    async validateLunchboxRestrictions(lunchboxId) {
        const response = await this.post(`/lunchboxes/${lunchboxId}/validate`);
        return await response.json();
    }

    // ========================================
    // MÉTODOS ESPECÍFICOS DE LONCHERAS
    // ========================================

    /**
     * Agrega item a lonchera con validación de restricciones
     * @param {number} lunchboxId - ID de la lonchera
     * @param {Object} item - { alimento_id, cantidad }
     * @returns {Promise<Object>}
     */
    async addItemToLunchbox(lunchboxId, item) {
        return await this.post(`/lunchboxes/${lunchboxId}/items`, item);
    }

    /**
     * Quita item de lonchera
     * @param {number} lunchboxId - ID de la lonchera
     * @param {number} alimentoId - ID del alimento
     * @returns {Promise<Response>}
     */
    async removeItemFromLunchbox(lunchboxId, alimentoId) {
        return await this.delete(`/lunchboxes/${lunchboxId}/items/${alimentoId}`);
    }
}

// ========================================
// INSTANCIA GLOBAL
// ========================================

const API = new APIClient(API_BASE_URL);

// ========================================
// EXPORTAR (si usas módulos)
// ========================================

// export default API;
// export { APIClient };