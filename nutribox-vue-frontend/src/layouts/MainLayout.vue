<template>
  <div class="d-flex" style="min-height: 100vh;">
    <aside class="sidebar bg-white shadow-sm p-4 d-flex flex-column" style="width: 260px;">
      <div class="sidebar-logo mb-4 fs-4 fw-bold text-primary-nb">🍃 NutriBox</div>
      <nav class="nav nav-pills flex-column sidebar-nav">
          <router-link to="/dashboard" class="nav-link text-dark" active-class="active"><i class="fas fa-home fa-fw me-2"></i> Dashboard</router-link>
          <router-link to="/hijos" class="nav-link text-dark" active-class="active"><i class="fas fa-child fa-fw me-2"></i> Mis Hijos</router-link>
          <router-link to="/crear-lonchera" class="nav-link text-dark" active-class="active"><i class="fas fa-plus-circle fa-fw me-2"></i> Crear Lonchera</router-link>
          <router-link to="/mis-loncheras" class="nav-link text-dark" active-class="active"><i class="fas fa-list fa-fw me-2"></i> Mis Loncheras</router-link>
          <router-link to="/direcciones" class="nav-link text-dark" active-class="active"><i class="fas fa-map-marker-alt fa-fw me-2"></i> Direcciones</router-link>
          <router-link to="/restricciones" class="nav-link text-dark" active-class="active"><i class="fas fa-ban fa-fw me-2"></i> Restricciones</router-link>
          <router-link to="/alimentos" class="nav-link text-dark" active-class="active"><i class="fas fa-utensils fa-fw me-2"></i> Alimentos</router-link>
          <router-link to="/menus" class="nav-link text-dark" active-class="active"><i class="fas fa-book-open fa-fw me-2"></i> Menus</router-link>
          <router-link to="/estadisticas" class="nav-link text-dark" active-class="active"><i class="fas fa-chart-line fa-fw me-2"></i> Estadisticas</router-link>
          <router-link to="/perfil" class="nav-link text-dark" active-class="active"><i class="fas fa-user-circle fa-fw me-2"></i> Mi Perfil</router-link>

          <router-link v-if="userData && userData.rol.nombre === 'Admin'" to="/admin/foods" class="nav-link text-dark mt-3" active-class="active">
              <i class="fas fa-cog fa-fw me-2"></i> Admin Panel
          </router-link>

          <a class="nav-link mt-auto" href="#" @click.prevent="logout"><i class="fas fa-sign-out-alt fa-fw me-2"></i> Cerrar Sesion</a>
      </nav>
    </aside>
    <main class="flex-grow-1 p-4 bg-light">
       <router-view />
    </main>
    </div>
</template>

<script setup>
// === INICIO: Script setup (pegado y adaptado) ===
import { ref, onMounted } from 'vue';
import { RouterView, useRouter } from 'vue-router'; // Importa RouterView
import { getUserDetail } from '@/utils/user';
import authService from '@/services/auth.service';

const router = useRouter();
const userData = ref(null); // Necesario para el link de Admin

const logout = () => {
  authService.logout();
  router.push('/login'); // Redirige a login al cerrar sesión
};

onMounted(() => {
    // Obtenemos los datos del usuario al montar el layout
    userData.value = getUserDetail();
});
// === FIN: Script setup ===
</script>

<style scoped>
  /* Puedes añadir estilos específicos para el layout si es necesario */
  /* Asegura que active-class funcione bien */
  .sidebar-nav .nav-link.active {
    background-color: var(--nb-primary, #43A047) !important; /* Usa variable CSS o color por defecto */
    color: white !important;
    font-weight: 600;
  }
  .nav-link.mt-auto {
    color: var(--nb-danger, #F44336); /* Color rojo para logout */
  }
  .nav-link.mt-auto:hover {
    background-color: rgba(244, 67, 54, 0.1); /* Fondo rojo suave al pasar */
  }
</style>