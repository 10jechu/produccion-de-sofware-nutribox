import { createRouter, createWebHistory } from 'vue-router'

// Importaciones de Vistas
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import HijosView from '../views/HijosView.vue'
import LoncherasView from '../views/LoncherasView.vue'
import CrearLoncheraView from '../views/CrearLoncheraView.vue'
import DireccionesView from '../views/DireccionesView.vue'
import RestriccionesView from '../views/RestriccionesView.vue'
import AlimentosView from '../views/AlimentosView.vue'
import PerfilView from '../views/PerfilView.vue'
import EstadisticasView from '../views/EstadisticasView.vue'
import MenusView from '../views/MenusView.vue'
import AdminView from '../views/AdminView.vue'

// Importación del Layout Principal
import MainLayout from '@/layouts/MainLayout.vue' // <-- Asegúrate que la ruta sea correcta

// Importaciones de Utilidades de Autenticación/Autorización
import { hasRequiredMembership, isAdmin, getUserDetail } from '@/utils/user';

const routes = [
  // --- Rutas Públicas (sin sidebar) ---
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },

  // --- Rutas Privadas (con sidebar persistente usando MainLayout) ---
  {
    path: '/',                     // Ruta padre para el layout
    component: MainLayout,         // Usa el componente MainLayout
    meta: { requiresAuth: true }, // Todas las rutas hijas requieren autenticación
    children: [
      {
        path: '/dashboard',
        name: 'dashboard',
        component: DashboardView
        // No necesita meta adicional si solo requiere Auth
      },
      {
        path: '/perfil',
        name: 'perfil',
        component: PerfilView
        // No necesita meta adicional
      },
      {
        path: '/hijos',
        name: 'hijos',
        component: HijosView
        // No necesita meta adicional
      },
      {
        path: '/direcciones',
        name: 'direcciones',
        component: DireccionesView
        // No necesita meta adicional
      },
      {
        path: '/crear-lonchera',
        name: 'crear-lonchera',
        component: CrearLoncheraView,
        meta: { requiredMembership: 'Estandar' } // Requiere al menos Estandar
      },
      {
        path: '/mis-loncheras',
        name: 'mis-loncheras',
        component: LoncherasView
        // No necesita meta adicional
      },
      {
        path: '/menus',
        name: 'menus',
        component: MenusView
        // No necesita meta adicional (la vista controla si se puede agregar)
      },
      {
        path: '/restricciones',
        name: 'restricciones',
        component: RestriccionesView,
        meta: { requiredMembership: 'Premium' } // Requiere Premium
      },
      {
        path: '/estadisticas',
        name: 'estadisticas',
        component: EstadisticasView,
        meta: { requiredMembership: 'Estandar' } // Requiere al menos Estandar
      },
      {
        path: '/alimentos',
        name: 'alimentos',
        component: AlimentosView
        // No necesita meta adicional (la vista controla si muestra botones de admin)
      },
      {
        path: '/admin/foods', // Ejemplo de ruta solo para admin
        name: 'admin-foods',
        component: AdminView, // O una vista específica de admin
        meta: { requiresAdmin: true } // Requiere rol Admin
      },
      // Redirección por defecto si se accede a '/' estando logueado
      {
        path: '', // Redirige de '/' a '/dashboard' DENTRO del layout
        redirect: '/dashboard'
      }
    ]
  }, // --- Fin de Rutas Privadas con Layout ---

  // --- Catch-all para rutas no encontradas ---
  // Redirige a login si la ruta no coincide con nada (o a dashboard si prefieres)
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// --- Lógica de Guardia de Navegación (Autorización) ---
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('nutribox_token');
  const user = getUserDetail(); // Obtiene detalles incluyendo rol y membresía

  // Verifica si *alguna* de las rutas coincidentes (incluyendo padres) requiere autenticación
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  // 1. Si requiere autenticación y no está logueado -> A Login
  if (requiresAuth && !isAuthenticated) {
    console.log('Guardia: Requiere Auth, no autenticado. Redirigiendo a Login.');
    next({ name: 'login' });
  }
  // 2. Si intenta ir a Login/Register estando logueado -> A Dashboard
  else if ((to.name === 'login' || to.name === 'register') && isAuthenticated) {
    console.log('Guardia: Autenticado, intentando ir a Login/Register. Redirigiendo a Dashboard.');
    next({ name: 'dashboard' });
  }
  // 3. Si requiere rol Admin y no lo tiene -> A Dashboard (o página "No Autorizado")
  else if (to.matched.some(record => record.meta.requiresAdmin) && (!user || !user.rol || user.rol.nombre !== 'Admin')) {
    console.error('Guardia: Acceso denegado. Rol Admin requerido.');
    next({ name: 'dashboard' }); // O crea una ruta 'unauthorized'
  }
  // 4. Si requiere una membresía específica y no la tiene -> A Dashboard (o página "Upgrade")
  else if (to.matched.some(record => record.meta.requiredMembership)) {
      // Encuentra el 'meta' más específico que define 'requiredMembership'
      const requiredPlanMeta = to.matched.slice().reverse().find(record => record.meta.requiredMembership);
      if (requiredPlanMeta && !hasRequiredMembership(requiredPlanMeta.meta.requiredMembership)) {
          console.error(`Guardia: Acceso denegado. Plan '${requiredPlanMeta.meta.requiredMembership}' requerido.`);
          next({ name: 'dashboard' }); // O crea una ruta 'upgrade-plan'
      } else {
          // Si tiene el plan o no se encontró un meta específico (poco probable), continúa
          next();
      }
  }
  // 5. Si pasa todas las validaciones -> Permite el acceso
  else {
    next();
  }
});

export default router;