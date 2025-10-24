// Verificar si está autenticado
const isAuthenticated = () => {
    return !!getToken();
};

// Redirigir a login si no está autenticado
const requireAuth = () => {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
    }
};

// Logout
const logout = () => {
    clearStorage();
    window.location.href = 'login.html';
};

// Mostrar notificación con SweetAlert2
const showNotification = (title, text, icon = 'success') => {
    Swal.fire({
        title,
        text,
        icon,
        confirmButtonColor: '#4CAF50'
    });
};

// Confirmar acción
const confirmAction = (title, text) => {
    return Swal.fire({
        title,
        text,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#4CAF50',
        cancelButtonColor: '#F44336',
        confirmButtonText: 'Sí, continuar',
        cancelButtonText: 'Cancelar'
    });
};

// Formatear fecha
const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

// Mostrar loading
const showLoading = () => {
    Swal.fire({
        title: 'Cargando...',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
};

// Cerrar loading
const closeLoading = () => {
    Swal.close();
};
