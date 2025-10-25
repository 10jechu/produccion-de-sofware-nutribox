// js/api.js - Helper para peticiones HTTP a la API de NutriBox

// ... (API_BASE_URL, APIClient class definition)

class APIClient {
    // ...

    /**
     * Obtiene el token de autenticación (llama a la función unificada)
     */
    getToken() {
        // 🚨 CRÍTICO: Usa la función global de config.js
        return getToken();
    }

    // ... (getHeaders sigue igual)

    /**
     * Maneja errores de las peticiones (ajustado para usar removeToken/removeUser)
     */
    async handleError(response) {
        let errorData;
        // ... (código de errorData)

        const error = new Error(errorData.detail || errorData.message || 'Error en la petición');
        // ...

        // Si es 401, redirigir al login
        if (response.status === 401) {
            // 🚨 CRÍTICO: Usa las funciones unificadas
            removeToken();
            removeUser();
            window.location.href = 'login.html';
        }

        throw error;
    }

    // ... (get, post, patch, delete siguen igual)

    // ========================================
    // MÉTODOS DE AUTENTICACIÓN
    // ========================================

    async login(email, password) {
        // ... (fetch code para obtener el token con formData)

        const data = await response.json();

        // 🚨 CRÍTICO: Usa las funciones unificadas
        saveToken(data.access_token);

        // Obtener datos del usuario
        const userResponse = await this.get('/users/me'); // Endpoint para obtener perfil
        const user = await userResponse.json();

        // 🚨 CRÍTICO: Usa la función unificada
        saveUser(user);

        return { token: data.access_token, user };
    }

    /**
     * Logout
     */
    logout() {
        // 🚨 CRÍTICO: Usa las funciones unificadas
        removeToken();
        removeUser();
        window.location.href = 'login.html';
    }

    // ... (El resto de la clase sigue igual)
}

const API = new APIClient(API_BASE_URL);