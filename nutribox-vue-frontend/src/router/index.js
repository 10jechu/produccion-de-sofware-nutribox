import { createRouter, createWebHistory } from 'vue-router'
// Importaremos las vistas aquí cuando las creemos
import HomeView from '../views/HomeView.vue' // Vista de ejemplo inicial
import LoginView from '../views/LoginView.vue' // Crearemos esta vista
import RegisterView from '../views/RegisterView.vue' // Crearemos esta vista
// Importaremos las vistas protegidas aquí
import DashboardView from '../views/DashboardView.vue'
// ... importar las demás vistas (HijosView, AlimentosView, etc.)

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Rutas Públicas
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
    // Ruta de ejemplo inicial (la eliminaremos o cambiaremos luego)
    {
      path: '/home-example', // Cambiado para evitar conflicto con la raíz
      name: 'home-example',
      component: HomeView
    },

    // --- Rutas Protegidas (requieren login) ---
    // Usaremos 'meta: { requiresAuth: true }' para marcarlas
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    // --- Añadiremos las demás rutas protegidas aquí ---
    // { path: '/hijos', name: 'hijos', component: HijosView, meta: { requiresAuth: true } },
    // ... (crear-lonchera, mis-loncheras, direcciones, etc.)
    // { path: '/perfil', name: 'perfil', component: PerfilView, meta: { requiresAuth: true } },


    // --- Redirecciones y Rutas por Defecto ---
    {
      path: '/', // La raíz ahora redirige a login
      redirect: '/login'
    },
    // Ruta Catch-all (404 o redirigir a dashboard)
    {
      path: '/:pathMatch(.*)*',
      redirect: '/dashboard' // O a un componente NotFoundView
    }
  ]
})

// --- Lógica de Guardia de Navegación (para proteger rutas) ---
// Esto se ejecutará antes de cada cambio de ruta
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('nutribox_token'); // Verifica si hay token

  if (to.meta.requiresAuth && !isAuthenticated) {
    // Si la ruta requiere autenticación y no hay token, redirige a login
    next({ name: 'login' });
  } else if ((to.name === 'login' || to.name === 'register') && isAuthenticated) {
    // Si intenta ir a login/register estando autenticado, redirige a dashboard
    next({ name: 'dashboard' });
  } else {
    // En cualquier otro caso, permite la navegación
    next();
  }
});

export default router