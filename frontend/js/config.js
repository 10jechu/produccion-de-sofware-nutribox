// js/config.js
// Configuración global (Todas las funciones de gestión de sesión están aquí)
const CONFIG = {
    API_BASE_URL: 'http://127.0.0.1:8000/api/v1',
    APP_NAME: 'NutriBox',
    VERSION: '2.0.0'
};

// Guardar token
const saveToken = (token) => {
    localStorage.setItem('nutribox_token', token);
};

// Obtener token
const getToken = () => {
    return localStorage.getItem('nutribox_token');
};

// Eliminar token
const removeToken = () => {
    localStorage.removeItem('nutribox_token');
};

// Guardar datos de usuario
const saveUser = (user) => {
    localStorage.setItem('nutribox_user', JSON.stringify(user));
};

// Obtener datos de usuario
const getUser = () => {
    const user = localStorage.getItem('nutribox_user');
    return user ? JSON.parse(user) : null;
};

// Función para remover solo el usuario
const removeUser = () => {
    localStorage.removeItem('nutribox_user');
};

// Función de limpieza total
const clearStorage = () => {
    localStorage.clear();
};