<script setup>
import { useRouter } from 'vue-router';
import authService from '@/services/auth.service';
import { getUserDetail, isAdmin, hasRequiredMembership } from '@/utils/user';
import { computed } from 'vue';

const router = useRouter();
const isUserAdmin = isAdmin();

// --- Computadas para control de vistas por plan ---
const canSeeEstandar = computed(() => hasRequiredMembership('Estandar'));
const canSeePremium = computed(() => hasRequiredMembership('Premium'));

const logout = () => {
  authService.logout();
  router.push('/login');
};
</script>

<template>
  <div class="d-flex" style="min-height: 100vh;">
    <aside class="sidebar bg-white shadow-sm p-4 d-flex flex-column" style="width: 260px;">
        <div class="sidebar-logo mb-4 fs-4 fw-bold text-primary-nb">🍃 NutriBox</div>
        <nav class="nav nav-pills flex-column sidebar-nav">

            <router-link v-if="!isUserAdmin" to="/dashboard" class="nav-link text-dark"><i class="fas fa-home fa-fw me-2"></i> Dashboard</router-link>
            
            <router-link v-if="!isUserAdmin && canSeeEstandar" to="/hijos" class="nav-link text-dark"><i class="fas fa-child fa-fw me-2"></i> Mis Hijos</router-link>
            <router-link v-if="!isUserAdmin && canSeePremium" to="/crear-lonchera" class="nav-link text-dark"><i class="fas fa-plus-circle fa-fw me-2"></i> Crear Lonchera</router-link>
            <router-link v-if="!isUserAdmin && canSeeEstandar" to="/mis-loncheras" class="nav-link text-dark"><i class="fas fa-list fa-fw me-2"></i> Mis Loncheras</router-link>
            <router-link v-if="!isUserAdmin && canSeeEstandar" to="/direcciones" class="nav-link text-dark"><i class="fas fa-map-marker-alt fa-fw me-2"></i> Direcciones</router-link>
            <router-link v-if="!isUserAdmin && canSeePremium" to="/restricciones" class="nav-link text-dark"><i class="fas fa-ban fa-fw me-2"></i> Restricciones</router-link>
            <router-link v-if="!isUserAdmin && canSeeEstandar" to="/estadisticas" class="nav-link text-dark"><i class="fas fa-chart-line fa-fw me-2"></i> Estadísticas</router-link>
            
            <router-link v-if="!isUserAdmin && canSeeEstandar" to="/alimentos" class="nav-link text-dark"><i class="fas fa-utensils fa-fw me-2"></i> Alimentos</router-link>
            <router-link v-if="!isUserAdmin" to="/menus" class="nav-link text-dark"><i class="fas fa-book-open fa-fw me-2"></i> Menús</router-link>
            
            <router-link to="/perfil" class="nav-link text-dark"><i class="fas fa-user-circle fa-fw me-2"></i> Mi Perfil</router-link>
            
            <router-link v-if="isUserAdmin" to="/admin/foods" class="nav-link text-dark mt-3">
                <i class="fas fa-cog fa-fw me-2"></i> Admin Panel
            </router-link>
            <a class="nav-link mt-auto" href="#" @click.prevent="logout"><i class="fas fa-sign-out-alt fa-fw me-2"></i> Cerrar Sesión</a>
        </nav>
    </aside>

    <slot />
  </div>
</template>

<style scoped>
.sidebar { height: 100vh; }
</style>
