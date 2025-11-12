// src/services/permissions.service.js

class PermissionsService {
    // Mapeo EXACTO basado en tu tabla de funcionalidades
    planPermissions = {
        'FREE': {
            // Visualización básica
            canViewFoods: true,
            canViewMenus: true,
            canViewRecipes: true,
            
            // Funciones bloqueadas
            canCreateLunchbox: false,
            canDeleteLunchbox: false,
            canManageAddresses: false,
            canViewStatistics: false,
            canCustomizeLunchbox: false,
            canViewHistory: false,
            canSetRestrictions: false,
            maxAddresses: 0,
            statsType: 'none',
            message: 'Plan Free - Solo visualización'
        },
        'ESTANDAR': {
            // Visualización básica
            canViewFoods: true,
            canViewMenus: true,
            canViewRecipes: true,
            
            // Funciones desbloqueadas
            canCreateLunchbox: true,
            canDeleteLunchbox: true,
            canManageAddresses: true,
            canViewStatistics: true,
            
            // Funciones bloqueadas
            canCustomizeLunchbox: false,
            canViewHistory: false,
            canSetRestrictions: false,
            
            // Límites
            maxAddresses: 1,
            statsType: 'basic', // Calorías y macros
            message: 'Plan Estándar - Funciones básicas'
        },
        'PREMIUM': {
            // Todas las funciones desbloqueadas
            canViewFoods: true,
            canViewMenus: true,
            canViewRecipes: true,
            canCreateLunchbox: true,
            canDeleteLunchbox: true,
            canManageAddresses: true,
            canViewStatistics: true,
            canCustomizeLunchbox: true,
            canViewHistory: true,
            canSetRestrictions: true,
            
            // Límites
            maxAddresses: 3,
            statsType: 'advanced', // Comparativas, tendencias
            message: 'Plan Premium - Todas las funciones'
        },
        'ADMIN': {
            // Permisos de administración
            canManageFoods: true,
            canManageMenus: true,
            canAccessAdmin: true,
            // Resto de funciones bloqueadas para admin
            canCreateLunchbox: false,
            canViewStatistics: false,
            canManageAddresses: false,
            message: 'Administrador'
        }
    };

    // Obtener permisos del usuario actual - COMPATIBLE con tu estructura
    getUserPermissions() {
        try {
            const user = this.getCurrentUser();
            if (!user) return this.planPermissions.FREE;
            
            // Si es admin, retornar permisos de admin
            if ((user.rol && user.rol.nombre === 'Admin') || user.rol === 'Admin') {
                return this.planPermissions.ADMIN;
            }
            
            // Obtener plan del usuario (membresía) - compatible con tu estructura
            const userPlan = (user.membresia && user.membresia.tipo) ? user.membresia.tipo : 'Free';
            const plan = userPlan.toUpperCase();
            
            return this.planPermissions[plan] || this.planPermissions.FREE;
        } catch (error) {
            console.warn('Error getting user permissions, defaulting to FREE:', error);
            return this.planPermissions.FREE;
        }
    }

    // Obtener usuario actual - compatible con tu utils/user.js
    getCurrentUser() {
        try {
            const userStr = localStorage.getItem('nutribox_user');
            return userStr ? JSON.parse(userStr) : null;
        } catch (error) {
            console.error('Error parsing user data:', error);
            localStorage.removeItem('nutribox_user');
            return null;
        }
    }

    // Verificar permiso específico
    hasPermission(permission) {
        const userPermissions = this.getUserPermissions();
        return userPermissions[permission] || false;
    }

    // Verificar si puede acceder a una ruta
    canAccessRoute(routeName) {
        const permissions = this.getUserPermissions();
        
        const routePermissions = {
            'dashboard': null, // Todos pueden acceder
            'hijos': 'canCreateLunchbox',
            'crear-lonchera': 'canCreateLunchbox',
            'mis-loncheras': 'canCreateLunchbox',
            'direcciones': 'canManageAddresses',
            'restricciones': 'canSetRestrictions',
            'alimentos': 'canViewFoods',
            'menus': 'canViewMenus',
            'estadisticas': 'canViewStatistics',
            'perfil': null, // Todos pueden acceder
            'admin': 'canAccessAdmin',
            'admin-foods': 'canManageFoods',
            'admin-menus': 'canManageMenus'
        };

        const requiredPermission = routePermissions[routeName];
        return !requiredPermission || permissions[requiredPermission];
    }

    // Verificar si es administrador (compatible con tu utils/user.js)
    isAdmin() {
        const user = this.getCurrentUser();
        return user && user.rol && user.rol.nombre === 'Admin';
    }

    // Mensaje para funciones bloqueadas
    getUpgradeMessage(featureName) {
        const user = this.getCurrentUser();
        const currentPlan = (user && user.membresia && user.membresia.tipo) ? user.membresia.tipo : 'Free';
        
        const upgradeMap = {
            'FREE': { 
                plan: 'Estándar o Premium', 
                features: ['Crear loncheras', 'Gestionar direcciones', 'Estadísticas básicas'] 
            },
            'ESTANDAR': { 
                plan: 'Premium', 
                features: ['Personalización avanzada', 'Historial', 'Restricciones', 'Estadísticas avanzadas'] 
            }
        };
        
        const upgradeInfo = upgradeMap[currentPlan.toUpperCase()] || { 
            plan: 'Premium', 
            features: ['Funciones premium'] 
        };
        
        return {
            message: `Para acceder a ${featureName} necesitas el plan ${upgradeInfo.plan}`,
            requiredPlan: upgradeInfo.plan,
            features: upgradeInfo.features
        };
    }

    // Verificar límite de direcciones
    canAddMoreAddresses(currentAddressCount) {
        const permissions = this.getUserPermissions();
        if (!permissions.canManageAddresses) return false;
        return currentAddressCount < permissions.maxAddresses;
    }

    // Obtener tipo de estadísticas permitidas
    getStatsType() {
        const permissions = this.getUserPermissions();
        return permissions.statsType || 'none';
    }

    // Obtener el plan actual del usuario
    getCurrentPlan() {
        const user = this.getCurrentUser();
        return (user && user.membresia && user.membresia.tipo) ? user.membresia.tipo : 'Free';
    }

    // Verificar si tiene membresía requerida (compatible con tu utils/user.js)
    hasRequiredMembership(requiredPlan) {
        const user = this.getCurrentUser();
        const userPlan = (user && user.membresia && user.membresia.tipo) ? user.membresia.tipo : 'Free';
        
        const tiers = {
            'Básico': 0,
            'Free': 0,
            'Estándar': 1,
            'Estandar': 1,
            'Premium': 2
        };
        
        const userTier = tiers[userPlan] !== undefined ? tiers[userPlan] : 0;
        const requiredTier = tiers[requiredPlan] !== undefined ? tiers[requiredPlan] : 0;
        
        return userTier >= requiredTier;
    }
}

export default new PermissionsService();