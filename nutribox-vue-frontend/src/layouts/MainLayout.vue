<template>
  <div class="app-layout">
    <!-- Sidebar Navigation -->
    <nav class="sidebar bg-success text-white">
      <div class="sidebar-header p-3">
        <router-link to="/app/dashboard" class="navbar-brand text-white">
          <i class="fas fa-utensils me-2"></i>
          <strong>NutriBox</strong>
        </router-link>
      </div>

      <ul class="sidebar-nav">
        <li class="nav-item">
          <router-link to="/app/dashboard" class="nav-link">
            <i class="fas fa-home me-2"></i>Dashboard
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/app/alimentos" class="nav-link">
            <i class="fas fa-utensils me-2"></i>Alimentos
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/app/menus" class="nav-link">
            <i class="fas fa-book-open me-2"></i>Menús Predeterminados
          </router-link>
        </li>

        <!-- Solo para usuarios NO Admin con plan Estándar/Premium -->
        <li class="nav-item" v-if="userData?.membresia?.tipo !== 'Free' && userData?.rol?.nombre !== 'Admin'">
          <router-link to="/app/mis-loncheras" class="nav-link">
            <i class="fas fa-briefcase me-2"></i>Mis Loncheras
          </router-link>
        </li>

        <li class="nav-item" v-if="userData?.membresia?.tipo !== 'Free' && userData?.rol?.nombre !== 'Admin'">
          <router-link to="/app/crear-lonchera" class="nav-link">
            <i class="fas fa-plus-circle me-2"></i>Crear Lonchera
          </router-link>
        </li>

        <!-- Solo para Admin -->
        <li class="nav-item" v-if="userData?.rol?.nombre === 'Admin'">
          <router-link to="/app/admin/foods" class="nav-link">
            <i class="fas fa-cog me-2"></i>Panel Admin
          </router-link>
        </li>

        <li class="nav-item">
          <router-link to="/app/perfil" class="nav-link">
            <i class="fas fa-user me-2"></i>Mi Perfil
          </router-link>
        </li>
      </ul>

      <div class="sidebar-footer p-3">
        <div class="user-info-small text-center mb-3">
          <small class="text-light opacity-75">Conectado como</small>
          <div class="fw-bold">{{ userData?.nombre || 'Usuario' }}</div>
          <div>
            <span :class="getMembershipBadgeClass(userData?.membresia?.tipo)" class="badge badge-sm">
              {{ userData?.membresia?.tipo || 'Free' }}
            </span>
            <span v-if="userData?.rol?.nombre === 'Admin'" class="badge bg-warning text-dark badge-sm ms-1">
              Admin
            </span>
          </div>
        </div>
        <button class="btn btn-outline-light btn-sm w-100" @click="logout">
          <i class="fas fa-sign-out-alt me-1"></i>Cerrar Sesión
        </button>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Top Header -->
      <header class="top-header bg-white shadow-sm">
        <div class="container-fluid">
          <div class="d-flex justify-content-between align-items-center py-3">
            <h4 class="mb-0">{{ currentRouteName }}</h4>
            <div class="user-info">
              <span class="me-3">Hola, {{ userData?.nombre || 'Usuario' }}</span>
              <span :class="getMembershipBadgeClass(userData?.membresia?.tipo)" class="badge">
                {{ userData?.membresia?.tipo || 'Free' }}
              </span>
              <span v-if="userData?.rol?.nombre === 'Admin'" class="badge bg-warning text-dark ms-2">
                Admin
              </span>
            </div>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <div class="content-wrapper">
        <router-view></router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { getUserDetail } from '@/utils/user';
import authService from '@/services/auth.service';

const router = useRouter();
const route = useRoute();
const userData = ref(null);

const currentRouteName = computed(() => {
  const routeNames = {
    'dashboard': 'Dashboard',
    'alimentos': 'Alimentos',
    'menus': 'Menús Predeterminados',
    'mis-loncheras': 'Mis Loncheras',
    'crear-lonchera': 'Crear Lonchera',
    'perfil': 'Mi Perfil',
    'admin-foods': 'Panel de Administración'
  };
  return routeNames[route.name] || 'NutriBox';
});

// Clases para badges de membresía
const getMembershipBadgeClass = (tipo) => {
  if (tipo === 'Premium') return 'bg-warning text-dark';
  if (tipo === 'Estandar') return 'bg-success text-white';
  return 'bg-secondary text-white';
};

const logout = () => {
  authService.logout();
  router.push('/login');
};

onMounted(() => {
  userData.value = getUserDetail();
});
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 250px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.sidebar-nav {
  flex: 1;
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin: 0;
}

.nav-link {
  color: rgba(255,255,255,0.8);
  padding: 12px 20px;
  display: block;
  text-decoration: none;
  transition: all 0.3s;
  border-left: 3px solid transparent;
}

.nav-link:hover, .nav-link.router-link-active {
  color: white;
  background: rgba(255,255,255,0.1);
  border-left-color: white;
}

.nav-link.router-link-active {
  font-weight: 600;
}

.sidebar-footer {
  border-top: 1px solid rgba(255,255,255,0.1);
}

.user-info-small {
  font-size: 0.875rem;
}

.badge-sm {
  font-size: 0.7em;
  padding: 0.25em 0.5em;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.top-header {
  border-bottom: 1px solid #dee2e6;
}

.content-wrapper {
  flex: 1;
  padding: 20px;
  background-color: #f8f9fa;
}
</style>