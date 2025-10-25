// js/utils.js
// IMPORTANTE: Asume que config.js está cargado antes y provee getToken, getUser, etc.

// ========================================
// GESTIÓN DE USUARIO (SOLO LÓGICA DE NEGOCIO/FLUJO)
// ========================================

function logout() {
    // 🚨 Usa las funciones unificadas de config.js
    removeToken();
    removeUser();
    window.location.href = 'login.html';
}

/**
 * Requiere autenticación - redirige a login si no hay usuario
 */
function requireAuth() {
    // 🚨 Llama a la función unificada getUser()
    const user = getUser();
    if (!user) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// ========================================
// SISTEMA DE PERMISOS (canUserDo, showUpgradeModal, etc.)
// ... (El resto del código de permisos se mantiene igual)
// ========================================

/**
 * Verifica si el usuario puede realizar una acción específica
 */
function canUserDo(action) {
    const user = getUser();
    if (!user || !user.membresia) return false;

    // Admin siempre puede todo
    if (user.rol && user.rol.nombre === 'Admin') return true;

    // Matriz de permisos por acción (simplificada para este fragmento)
    const permissions = {
        'create_food': ['Premium'],
        'edit_food': ['Premium'],
        'customize_lunchbox': ['Premium'],
        'configure_restrictions': ['Estandar', 'Premium'],
        'add_lunchbox': ['Estandar', 'Premium'],
    };

    const requiredPlans = permissions[action];
    if (!requiredPlans) return false;

    return requiredPlans.includes(user.membresia.tipo);
}

// ... (El resto de funciones de permisos: getUserPlan, isAdmin, getAddressLimit)

/**
 * Muestra modal de actualización de plan
 */
function showUpgradeModal(feature = 'esta función') {
    const user = getUser();
    const currentPlan = user && user.membresia ? user.membresia.tipo : 'Free';

    Swal.fire({
        icon: 'info',
        title: 'Funcionalidad Premium',
        html: `<p>Tu plan actual <strong>${currentPlan}</strong> no incluye acceso a: <strong>${feature}</strong>.</p>`,
        showCancelButton: true,
        confirmButtonText: 'Ver Planes',
        confirmButtonColor: '#4CAF50'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = 'planes.html';
        }
    });
}

// ========================================
// LOADING (Restauradas para solucionar el ReferenceError)
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
// NOTIFICACIONES (Restauradas para solucionar el ReferenceError)
// ========================================

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

// ... (El resto de utilidades como confirmAction, formatDate, formatNumber, applyPermissions)