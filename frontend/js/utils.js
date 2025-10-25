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

    // Beneficios por plan
    const benefits = {
        'Estandar': [
            '✅ Crear loncheras predeterminadas',
            '✅ 1 dirección de entrega',
            '✅ Configurar restricciones alimentarias',
            '✅ Estadísticas básicas',
            '✅ Historial de loncheras'
        ],
        'Premium': [
            '✅ Personalización completa de loncheras',
            '✅ Gestión de alimentos personalizados',
            '✅ Hasta 3 direcciones de entrega',
            '✅ Estadísticas avanzadas con gráficos',
            '✅ Historial completo y restauración',
            '✅ Soporte prioritario',
            '✅ Todas las funciones desbloqueadas'
        ]
    };

    // Determinar plan sugerido
    const suggestedPlan = currentPlan === 'Free' ? 'Estandar' : 'Premium';

    Swal.fire({
        icon: 'info',
        title: `${feature} requiere plan ${suggestedPlan}`,
        html: `
            <div style="text-align: left; padding: 0 20px;">
                <p style="margin-bottom: 10px;">
                    <strong>Tu plan actual:</strong>
                    <span style="color: #FF9800;">${currentPlan}</span>
                </p>
                <p style="margin-bottom: 10px;">
                    <strong>Mejora a ${suggestedPlan} y obtén:</strong>
                </p>
                <ul style="list-style: none; padding-left: 0;">
                    ${benefits[suggestedPlan].map(b => `<li style="margin: 8px 0;">${b}</li>`).join('')}
                </ul>
                ${suggestedPlan === 'Premium' ? `
                    <div style="background: #FFF3E0; padding: 12px; border-radius: 8px; margin-top: 16px;">
                        <p style="margin: 0; font-size: 14px;">
                            💡 <strong>Recomendación:</strong> El plan Premium es ideal para
                            familias que quieren control total sobre la alimentación de sus hijos.
                        </p>
                    </div>
                ` : ''}
            </div>
        `,
        showCancelButton: true,
        confirmButtonText: `Ver Plan ${suggestedPlan}`,
        cancelButtonText: 'Tal vez después',
        confirmButtonColor: '#4CAF50',
        cancelButtonColor: '#9E9E9E',
        width: 600
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = 'planes.html';
        }
    });
}

// ========================================
// BADGE DE PLAN
// ========================================

/**
 * Renderiza badge del plan en el navbar/sidebar
 */
function renderPlanBadge() {
    const user = getUser();
    if (!user) return;

    const plan = user.membresia ? user.membresia.tipo : 'Free';

    const colors = {
        'Free': {
            bg: '#9E9E9E',
            text: '#FFFFFF'
        },
        'Estandar': {
            bg: '#2196F3',
            text: '#FFFFFF'
        },
        'Premium': {
            bg: 'linear-gradient(135deg, #FFD700 0%, #FFA500 100%)',
            text: '#000000'
        }
    };

    const style = colors[plan];

    const badge = `
        <div class="plan-badge" style="
            background: ${style.bg};
            color: ${style.text};
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            margin: 12px 0;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            ${plan === 'Premium' ? '⭐ ' : ''}${plan}
            ${plan !== 'Premium' ? '<span style="font-size: 10px; opacity: 0.8;"> ▸ <a href="planes.html" style="color: inherit; text-decoration: underline;">Mejorar</a></span>' : ''}
        </div>
    `;

    // Buscar dónde insertar el badge
    const sidebar = document.querySelector('.sidebar-logo') ||
                    document.querySelector('.user-info') ||
                    document.querySelector('nav');

    if (sidebar) {
        // Remover badge anterior si existe
        const oldBadge = document.querySelector('.plan-badge');
        if (oldBadge) oldBadge.remove();

        sidebar.insertAdjacentHTML('afterend', badge);
    }
}

// ========================================
// NOTIFICACIONES
// ========================================

/**
 * Muestra notificación toast
 * @param {string} title - Título
 * @param {string} message - Mensaje
 * @param {string} type - 'success', 'error', 'warning', 'info'
 */
function showNotification(title, message, type = 'info') {
    const icons = {
        'success': 'success',
        'error': 'error',
        'warning': 'warning',
        'info': 'info'
    };

    Swal.fire({
        icon: icons[type],
        title: title,
        text: message,
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
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

    // Verificar sesión
    const user = getUser();
    if (!user && !window.location.pathname.includes('login.html')) {
        window.location.href = 'login.html';
    }
});

// ========================================
// EXPORTAR FUNCIONES
// ========================================

// Si usas módulos ES6, puedes exportar así:
// export { canUserDo, showUpgradeModal, renderPlanBadge, ... };