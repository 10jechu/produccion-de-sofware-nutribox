<template>
  <div class="d-flex" style="min-height: 100vh;">
    <aside class="sidebar bg-card shadow-sm p-4 d-flex flex-column" style="width: 260px; position: sticky; top: 0; height: 100vh; overflow-y: auto;">
      <div class="sidebar-logo mb-4 fs-4 fw-bold text-dark-nb">🍃 NutriBox</div>
      <nav class="nav nav-pills flex-column sidebar-nav">
          <!-- Rutas básicas para todos -->
          <router-link to="/app/dashboard" class="nav-link text-dark-nb" active-class="active">
            <i class="fas fa-home fa-fw me-2"></i> Dashboard
          </router-link>
          
          <!-- Rutas con permisos -->
          <router-link v-if="canAccess('hijos')" to="/app/hijos" class="nav-link text-dark-nb" active-class="active">
            <i class="fas fa-child fa-fw me-2"></i> Mis Hijos
          </router-link>
          
          <router-link v-if="canAccess('crear-lonchera')" to="/app/crear-lonchera" class="nav-link text-dark-nb" active-class="active">
            <i class="fas fa-plus-circle fa-fw me-2"></i> Crear Lonchera
          </router-link>
          
          <router-link v-if="canAccess('mis-loncheras')" to="/app/mis-loncheras" class="nav-link text-dark-nb" active-class="active">
            <i class="fas fa-list fa-fw me-2"></i> Mis Loncheras
          </router-link>
          
          <router-link v-if="canAccess('direcciones')" to="/app/direcciones" class="nav-link text-dark-nb" active-class="active">
            <i class="fas fa-map-marker-alt fa-fw me-2"></i> Direcciones
          </router-link>
          
          <router-link v-if="canAccess('restricciones')" to="/app/restricciones" class="nav-link text-dark-nb" active-class="active">
            <i class="fas fa-ban fa-fw me-2"></i> Restricciones
          </router-link>
          
          <!-- Rutas de visualización -->
          <router-link to="/app/alimentos" class="nav-link text-dark-nb" active-class="active">
            <i class="fas fa-utensils fa-fw me-2"></i> Alimentos
          </router-link>
          
          <router-link to="/app/menus" class="nav-link text-dark-nb" active-class="active">
            <i class="fas fa-book-open fa-fw me-2"></i> Menús
          </router-link>
          
          <router-link v-if="canAccess('estadisticas')" to="/app/estadisticas" class="nav-link text-dark-nb" active-class="active">
            <i class="fas fa-chart-line fa-fw me-2"></i> Estadísticas
          </router-link>
          
          <router-link to="/app/perfil" class="nav-link text-dark-nb" active-class="active">
            <i class="fas fa-user-circle fa-fw me-2"></i> Mi Perfil
          </router-link>

          <!-- Admin Panel -->
          <router-link v-if="permissions.isAdmin()" to="/admin" class="nav-link text-dark-nb mt-3" active-class="active">
            <i class="fas fa-cog fa-fw me-2"></i> Admin Panel
          </router-link>

          <a class="nav-link mt-auto" href="#" @click.prevent="logout">
            <i class="fas fa-sign-out-alt fa-fw me-2"></i> Cerrar Sesión
          </a>
      </nav>
    </aside>
    
    <main class="flex-grow-1 p-4 bg-light-nb">
       <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getUserDetail } from '@/utils/user';
import authService from '@/services/auth.service';
import permissionsService from '@/services/permissions.service';

const router = useRouter();
const userData = ref(null);
const permissions = permissionsService;

const canAccess = (routeName) => {
  return permissions.canAccessRoute(routeName);
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
.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-nav .nav-link.active {
  background-color: var(--primary, #1F8D45) !important; 
  color: white !important;
  font-weight: 600;
}

.nav-link.mt-auto {
  color: var(--nb-danger, #E53935);
}

.nav-link.mt-auto:hover {
  background-color: rgba(229, 57, 53, 0.1);
}
</style>

