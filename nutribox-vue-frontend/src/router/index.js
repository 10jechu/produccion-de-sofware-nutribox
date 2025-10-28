import { createRouter, createWebHistory } from 'vue-router'
import { hasRequiredMembership, isAdmin, getUserDetail } from '@/utils/user';
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

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    
    { path: '/dashboard', name: 'dashboard', component: DashboardView, meta: { requiresAuth: true } },
    { path: '/perfil', name: 'perfil', component: PerfilView, meta: { requiresAuth: true } },
    
    { path: '/hijos', name: 'hijos', component: HijosView, meta: { requiresAuth: true } },
    { path: '/direcciones', name: 'direcciones', component: DireccionesView, meta: { requiresAuth: true } },
    
    { path: '/crear-lonchera', name: 'crear-lonchera', component: CrearLoncheraView, meta: { requiresAuth: true, requiredMembership: 'Estandar' } },
    { path: '/mis-loncheras', name: 'mis-loncheras', component: LoncherasView, meta: { requiresAuth: true } },
    { path: '/menus', name: 'menus', component: MenusView, meta: { requiresAuth: true } },
    
    { path: '/restricciones', name: 'restricciones', component: RestriccionesView, meta: { requiresAuth: true, requiredMembership: 'Premium' } },
    { path: '/estadisticas', name: 'estadisticas', component: EstadisticasView, meta: { requiresAuth: true, requiredMembership: 'Estandar' } },
    
    { path: '/alimentos', name: 'alimentos', component: AlimentosView, meta: { requiresAuth: true } },
    
    { path: '/admin/foods', name: 'admin-foods', component: AdminView, meta: { requiresAuth: true, requiresAdmin: true } },


    { path: '/', redirect: '/dashboard' }, 
    { path: '/:pathMatch(.*)*', redirect: '/dashboard' } 
  ]
})

// Lógica de Guardia de Navegación (Autorización)
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('nutribox_token');
  const user = getUserDetail(); 

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login' });
  } else if ((to.name === 'login' || to.name === 'register') && isAuthenticated) {
    next({ name: 'dashboard' });
  } else if (to.meta.requiresAdmin && (!user || !user.rol || user.rol.nombre !== 'Admin')) {
     console.error('Acceso denegado. Rol Admin requerido.');
     next({ name: 'dashboard' }); 
  } else if (to.meta.requiredMembership && !hasRequiredMembership(to.meta.requiredMembership)) {
    console.error('Acceso denegado. Plan ' + to.meta.requiredMembership + ' requerido.');
    next({ name: 'dashboard' });
  } else {
    next();
  }
});

export default router
