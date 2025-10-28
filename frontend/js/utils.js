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

//Date
const formatDate = (dateString) => {
    // Divide la fecha YYYY-MM-DD para evitar problemas de zona horaria
    const parts = dateString.split('-');
    // Crea la fecha usando UTC para asegurar que no cambie el día
    // Nota: El mes en el constructor de Date es 0-indexado (0=Enero, 1=Febrero, ...)
    const date = new Date(Date.UTC(parts[0], parts[1] - 1, parts[2]));

    return date.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        timeZone: 'UTC' // Importante: Formatea usando UTC para consistencia
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
