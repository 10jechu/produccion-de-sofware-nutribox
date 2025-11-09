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
import LandingView from '../views/LandingView.vue' // <-- VISTA DE PORTADA

// Importación del Layout Principal
import MainLayout from '@/layouts/MainLayout.vue'
// Importaciones de Utilidades de Autenticación/Autorización
import { hasRequiredMembership, isAdmin, getUserDetail } from '@/utils/user';

const routes = [
  // --- Ruta Principal / Portada (PÚBLICA) ---
  {
    path: '/',
    name: 'home',
    component: LandingView // Carga la vista de Landing
  },
  
  // --- Rutas Públicas de Auth ---
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

  // --- Rutas Privadas (agrupadas bajo /app) ---
  {
    path: '/app', // Base para rutas privadas
    component: MainLayout,
    meta: { requiresAuth: true }, // Todas las rutas hijas requieren autenticación
    children: [
      {
        path: 'dashboard', // /app/dashboard
        name: 'dashboard',
        component: DashboardView
      },
      {
        path: 'perfil', // /app/perfil
        name: 'perfil',
        component: PerfilView
      },
      {
        path: 'hijos',
        name: 'hijos',
        component: HijosView
      },
      {
        path: 'direcciones',
        name: 'direcciones',
        component: DireccionesView
      },
      {
        path: 'crear-lonchera',
        name: 'crear-lonchera',
        component: CrearLoncheraView,
        meta: { requiredMembership: 'Estandar' }
      },
      {
        path: 'mis-loncheras',
        name: 'mis-loncheras',
        component: LoncherasView
      },
      {
        path: 'menus',
        name: 'menus',
        component: MenusView
      },
      {
        path: 'restricciones',
        name: 'restricciones',
        component: RestriccionesView,
        meta: { requiredMembership: 'Premium' }
      },
      {
        path: 'estadisticas',
        name: 'estadisticas',
        component: EstadisticasView,
        meta: { requiredMembership: 'Estandar' }
      },
      {
        path: 'alimentos',
        name: 'alimentos',
        component: AlimentosView
      },
      {
        path: 'admin/foods',
        name: 'admin-foods',
        component: AdminView,
        meta: { requiresAdmin: true }
      },
    ]
  },
  
  // --- Catch-all para rutas no encontradas (redirige a la portada) ---
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// --- Lógica de Guardia de Navegación (Autorización) ---
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('nutribox_token');
  const user = getUserDetail();
  
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  // 1. Si requiere autenticación y no está logueado -> A Login
  if (requiresAuth && !isAuthenticated) {
    next({ name: 'login' });
  }
  // 2. Si intenta ir a Login/Register/Home estando logueado -> A Dashboard
  else if ((to.name === 'login' || to.name === 'register' || to.name === 'home') && isAuthenticated) {
    next({ name: 'dashboard' });
  }
  // 3. Si no es autenticado, permite el acceso a rutas públicas (home, login, register)
  //    Si es autenticado, pasa a la verificación de rol/membresía (dentro del else)
  else {
    // Verificación de roles/membresías para rutas privadas (/app/...)
    if (to.matched.some(record => record.meta.requiresAdmin) && (!user || !user.rol || user.rol.nombre !== 'Admin')) {
        next({ name: 'dashboard' });
    }
    else if (to.matched.some(record => record.meta.requiredMembership)) {
        const requiredPlanMeta = to.matched.slice().reverse().find(record => record.meta.requiredMembership);
        if (requiredPlanMeta && !hasRequiredMembership(requiredPlanMeta.meta.requiredMembership)) {
            next({ name: 'dashboard' });
        } else {
            next();
        }
    } else {
        next();
    }
  }
});

export default router;
