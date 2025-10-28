// js/api.js - Helper para peticiones HTTP a la API de NutriBox
// NOTA: ASUME que config.js está cargado ANTES y define las funciones
// saveToken, removeToken, removeUser, getToken, saveUser, y la constante CONFIG.

// ========================================
// CLASE API
// ========================================

class APIClient {
    // 🚨 CORRECCIÓN CRÍTICA: Inicializa baseURL usando CONFIG.API_BASE_URL
    constructor(baseURL) {
        // Usa la URL pasada o la URL de CONFIG si no se pasa ninguna.
        this.baseURL = baseURL || CONFIG.API_BASE_URL;
    }

    /**
     * Obtiene el token de autenticación (llama a la función unificada)
     */
    getToken() {
        return getToken();
    }

    /**
     * Obtiene los headers por defecto
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
            removeToken();
            removeUser();
            window.location.href = 'login.html';
        }
        throw error;
    }

    /**
     * Petición GET
     */
    async get(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'GET',
                headers: this.getHeaders(),
                ...options
            });

            if (!response.ok) { await this.handleError(response); }
            return response;
        } catch (error) {
            console.error('GET Error:', error);
            throw error;
        }
    }

    /**
     * Petición POST
     */
    async post(endpoint, data, options = {}) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify(data),
                ...options
            });

            if (!response.ok) { await this.handleError(response); }
            return response;
        } catch (error) {
            console.error('POST Error:', error);
            throw error;
        }
    }

    // ... (Métodos PATCH y DELETE omitidos por brevedad, asumiendo estructura similar)

    // ========================================
    // MÉTODOS DE AUTENTICACIÓN
    // ========================================

    async login(email, password) {
        try {
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            const response = await fetch(`${this.baseURL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData
            });

            if (!response.ok) { await this.handleError(response); }

            const data = await response.json();
            saveToken(data.access_token);

            // Obtener datos del usuario
            const userResponse = await this.get('/users/me');
            const user = await userResponse.json();
            saveUser(user);

            return { token: data.access_token, user };

        } catch (error) {
            console.error('Login Error:', error);
            throw error;
        }
    }

    async register(userData) {
        try {
            const response = await fetch(`${this.baseURL}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });

            if (!response.ok) { await this.handleError(response); }
            return await response.json();

        } catch (error) {
            console.error('Register Error:', error);
            throw error;
        }
    }

// ... (El resto de los métodos como login y register)

    /**
     * Logout
     */
    logout() {
        removeToken();
        removeUser();
        window.location.href = 'login.html';
    }

    // --- CORRECCIÓN AQUÍ ---
    // ESTA FUNCIÓN VA ANTES DEL CIERRE DE LA CLASE
    async getUserDetail(userId) {
        try {
            // Llama al endpoint del backend que SÍ existe
            const response = await this.get(`/users/${userId}/detail`);
            return await response.json();
        } catch (error) {
            console.error('Error fetching user detail:', error);
            throw error;
        }
    }
    // --- FIN DE LA CORRECCIÓN ---

} // <-- ESTA es la llave que cierra la 'class APIClient'

// 🚨 CORRECCIÓN CRÍTICA: Inicializa la instancia sin pasar un argumento,
// forzando que use el valor predeterminado de CONFIG.js.
const API = new APIClient();