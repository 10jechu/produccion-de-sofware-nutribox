<template>
  <div class="d-flex" style="min-height: 100vh;">
    <aside class="sidebar bg-card shadow-sm p-4 d-flex flex-column" style="width: 260px;">
      <div class="sidebar-logo mb-4 fs-4 fw-bold text-dark-nb">🍃 NutriBox</div>
      <nav class="nav nav-pills flex-column sidebar-nav">
          <router-link to="/app/dashboard" class="nav-link text-dark-nb" active-class="active"><i class="fas fa-home fa-fw me-2"></i> Dashboard</router-link>
          <router-link to="/app/hijos" class="nav-link text-dark-nb" active-class="active"><i class="fas fa-child fa-fw me-2"></i> Mis Hijos</router-link>
          <router-link to="/app/crear-lonchera" class="nav-link text-dark-nb" active-class="active"><i class="fas fa-plus-circle fa-fw me-2"></i> Crear Lonchera</router-link>
          <router-link to="/app/mis-loncheras" class="nav-link text-dark-nb" active-class="active"><i class="fas fa-list fa-fw me-2"></i> Mis Loncheras</router-link>
          <router-link to="/app/direcciones" class="nav-link text-dark-nb" active-class="active"><i class="fas fa-map-marker-alt fa-fw me-2"></i> Direcciones</router-link>
          <router-link to="/app/restricciones" class="nav-link text-dark-nb" active-class="active"><i class="fas fa-ban fa-fw me-2"></i> Restricciones</router-link>
          <router-link to="/app/alimentos" class="nav-link text-dark-nb" active-class="active"><i class="fas fa-utensils fa-fw me-2"></i> Alimentos</router-link>
          <router-link to="/app/menus" class="nav-link text-dark-nb" active-class="active"><i class="fas fa-book-open fa-fw me-2"></i> Menús</router-link>
          <router-link to="/app/estadisticas" class="nav-link text-dark-nb" active-class="active"><i class="fas fa-chart-line fa-fw me-2"></i> Estadísticas</router-link>
          <router-link to="/app/perfil" class="nav-link text-dark-nb" active-class="active"><i class="fas fa-user-circle fa-fw me-2"></i> Mi Perfil</router-link>

          <router-link v-if="userData && userData.rol.nombre === 'Admin'" to="/admin/foods" class="nav-link text-dark-nb mt-3" active-class="active">
              <i class="fas fa-cog fa-fw me-2"></i> Admin Panel
          </router-link>

          <a class="nav-link mt-auto" href="#" @click.prevent="logout"><i class="fas fa-sign-out-alt fa-fw me-2"></i> Cerrar Sesión</a>
      </nav>
    </aside>
    <main class="flex-grow-1 p-4 bg-light-nb">
       <router-view />
    </main>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { RouterView, useRouter } from 'vue-router';
import { getUserDetail } from '@/utils/user';
import authService from '@/services/auth.service';

const router = useRouter();
const userData = ref(null);

const logout = () => {
  authService.logout();
  router.push('/login'); // Redirige a login al cerrar sesión
};

onMounted(() => {
    // Obtenemos los datos del usuario al montar el layout
    userData.value = getUserDetail();
});
</script>

<style scoped>
  /* Asegura que active-class funcione bien */
  .sidebar-nav .nav-link.active {
    background-color: var(--primary, #1F8D45) !important; 
    color: white !important;
    font-weight: 600;
  }
  .nav-link.mt-auto {
    color: var(--nb-danger, #E53935); /* Color rojo para logout */
  }
  .nav-link.mt-auto:hover {
    background-color: rgba(229, 57, 53, 0.1); /* Fondo rojo suave al pasar */
  }
</style>
