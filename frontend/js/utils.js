// utils.js - Funciones de utilidad para NutriBox

// ========================================
// GESTIÓN DE USUARIO
// ========================================

function getUser() {
    const userStr = localStorage.getItem('user');
    if (!userStr) return null;
    return JSON.parse(userStr);
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

/**
 * Requiere autenticación - redirige a login si no hay usuario
 */
function requireAuth() {
    const user = getUser();
    if (!user) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// ========================================
// SISTEMA DE PERMISOS
// ========================================

/**
 * Verifica si el usuario puede realizar una acción específica
 * @param {string} action - Acción a verificar
 * @returns {boolean}
 */
function canUserDo(action) {
    const user = getUser();
    if (!user || !user.membresia) return false;

    // Admin siempre puede todo
    if (user.rol && user.rol.nombre === 'Admin') return true;

    // Matriz de permisos por acción
    const permissions = {
        'create_food': ['Premium'],
        'edit_food': ['Premium'],
        'delete_food': ['Premium'],
        'customize_lunchbox': ['Premium'],
        'configure_restrictions': ['Estandar', 'Premium'],
        'add_lunchbox': ['Estandar', 'Premium'],
        'view_advanced_stats': ['Premium'],
        'manage_multiple_addresses': ['Premium'],
        'view_basic_stats': ['Estandar', 'Premium'],
        'view_menus': ['Free', 'Estandar', 'Premium']
    };

    const requiredPlans = permissions[action];
    if (!requiredPlans) return false;

    return requiredPlans.includes(user.membresia.tipo);
}

/**
 * Obtiene el plan del usuario actual
 * @returns {string} 'Free', 'Estandar', 'Premium', o null
 */
function getUserPlan() {
    const user = getUser();
    if (!user || !user.membresia) return null;
    return user.membresia.tipo;
}

/**
 * Verifica si el usuario es administrador
 * @returns {boolean}
 */
function isAdmin() {
    const user = getUser();
    return user && user.rol && user.rol.nombre === 'Admin';
}

/**
 * Obtiene el límite de direcciones según el plan
 * @returns {number}
 */
function getAddressLimit() {
    const user = getUser();
    if (!user || !user.membresia) return 0;

    const limits = {
        'Free': 0,
        'Estandar': 1,
        'Premium': 3
    };

    return limits[user.membresia.tipo] || 0;
}

// ========================================
// MODAL DE UPGRADE
// ========================================

/**
 * Muestra modal de actualización de plan
 * @param {string} feature - Nombre de la funcionalidad bloqueada
 */
function showUpgradeModal(feature = 'esta función') {
    const user = getUser();
    const currentPlan = user && user.membresia ? user.membresia.tipo : 'Free';

    Swal.fire({
        icon: 'info',
        title: 'Funcionalidad Premium',
        html: `
            <p>Tu plan actual <strong>${currentPlan}</strong> no incluye acceso a: <strong>${feature}</strong>.</p>
            <p>Actualiza tu membresía para desbloquear esta y otras funcionalidades.</p>
        `,
        showCancelButton: true,
        confirmButtonText: 'Ver Planes',
        cancelButtonText: 'Cerrar',
        confirmButtonColor: '#4CAF50'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = 'planes.html';
        }
    });
}

/**
 * Renderiza el badge del plan en el header
 */
function renderPlanBadge() {
    const planBadge = document.getElementById('planBadge');
    if (!planBadge) return;

    const user = getUser();
    if (!user || !user.membresia) {
        planBadge.style.display = 'none';
        return;
    }

    const planColors = {
        'Free': '#9E9E9E',
        'Estandar': '#2196F3',
        'Premium': '#FFD700'
    };

    planBadge.textContent = user.membresia.tipo;
    planBadge.style.backgroundColor = planColors[user.membresia.tipo] || '#9E9E9E';
    planBadge.style.display = 'inline-block';
}

// ========================================
// NOTIFICACIONES
// ========================================

/**
 * Muestra una notificación usando SweetAlert2
 * @param {string} title - Título de la notificación
 * @param {string} text - Texto de la notificación
 * @param {string} icon - Tipo de icono: 'success', 'error', 'warning', 'info'
 */
function showNotification(title, text, icon = 'info') {
    Swal.fire({
        icon: icon,
        title: title,
        text: text,
        confirmButtonColor: '#4CAF50',
        timer: 3000,
        timerProgressBar: true
    });
}

/**
 * Muestra un diálogo de confirmación
 * @param {string} title - Título del diálogo
 * @param {string} text - Texto del diálogo
 * @returns {Promise} Promesa con el resultado
 */
function confirmAction(title, text) {
    return Swal.fire({
        icon: 'warning',
        title: title,
        text: text,
        showCancelButton: true,
        confirmButtonText: 'Sí, continuar',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#4CAF50',
        cancelButtonColor: '#F44336'
    });
}

// ========================================
// LOADING
// ========================================

let loadingInstance = null;

function showLoading(message = 'Cargando...') {
    loadingInstance = Swal.fire({
        title: message,
        allowOutsideClick: false,
        allowEscapeKey: false,
        showConfirmButton: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
}

function closeLoading() {
    if (loadingInstance) {
        Swal.close();
        loadingInstance = null;
    }
}

// ========================================
// FORMATEO
// ========================================

/**
 * Formatea fecha a string legible
 * @param {string} dateStr - Fecha en formato ISO
 * @returns {string}
 */
function formatDate(dateStr) {
    if (!dateStr) return '-';
    const date = new Date(dateStr);
    return date.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Formatea número con separador de miles
 * @param {number} num - Número
 * @returns {string}
 */
function formatNumber(num) {
    return new Intl.NumberFormat('es-CO').format(num);
}

// ========================================
// VALIDACIÓN DE PERMISOS EN BOTONES
// ========================================

/**
 * Deshabilita botones según permisos del usuario
 * Agregar atributo data-requires-permission="action" a los botones
 */
function applyPermissions() {
    document.querySelectorAll('[data-requires-permission]').forEach(button => {
        const action = button.getAttribute('data-requires-permission');

        if (!canUserDo(action)) {
            button.disabled = true;
            button.classList.add('btn-locked');
            button.innerHTML = '<i class="fas fa-lock"></i> ' + button.textContent.trim();
            button.onclick = (e) => {
                e.preventDefault();
                showUpgradeModal();
            };
        }
    });
}

// ========================================
// INICIALIZACIÓN
// ========================================

// Ejecutar al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    // Renderizar badge de plan
    renderPlanBadge();

    // Aplicar permisos a botones
    applyPermissions();

    // Verificar sesión solo en páginas que no son login/register/index
    const currentPage = window.location.pathname;
    const publicPages = ['login.html', 'register.html', 'index.html', '/'];
    const isPublicPage = publicPages.some(page => currentPage.includes(page) || currentPage === '/');

    if (!isPublicPage) {
        const user = getUser();
        if (!user) {
            window.location.href = 'login.html';
        }
    }
});