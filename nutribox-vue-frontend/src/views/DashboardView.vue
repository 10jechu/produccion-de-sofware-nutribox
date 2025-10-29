<script setup>
// Imports necesarios SOLO para el contenido del Dashboard
import { ref, onMounted } from 'vue';
import { getUserDetail } from '@/utils/user';
// Ya NO necesitas importar useRouter ni authService aquí para el logout

const userData = ref(null);
const isLoading = ref(true);

// Función para cargar los datos específicos del Dashboard
const loadDashboard = async () => {
  isLoading.value = true;
  const user = getUserDetail(); // Obtiene los datos del usuario (ya deberían estar en localStorage)

  if (!user) {
    // Si no hay datos de usuario, podrías manejarlo (aunque la guardia del router ya protege)
    console.error("Dashboard: No se encontraron datos del usuario.");
    // Podrías redirigir a login si es necesario, aunque el layout/guardia lo haría
    // import authService from '@/services/auth.service';
    // import { useRouter } from 'vue-router';
    // const router = useRouter();
    // authService.logout();
    // router.push('/login');
    isLoading.value = false;
    return;
  }
  // Asigna los datos del usuario para usarlos en la plantilla
  userData.value = user;
  isLoading.value = false;
};

// Función auxiliar para clases de badge (se queda aquí porque se usa en la plantilla)
const getMembershipBadgeClass = (tipo) => {
  if (tipo === 'Premium') {
    return 'bg-warning text-dark';
  } else if (tipo === 'Estandar') { // Asegúrate que coincida con el nombre en tus datos
    return 'bg-info';
  } else { // Asume Básico o Free
    return 'bg-secondary';
  }
};

// Carga los datos cuando el componente se monta
onMounted(() => {
  loadDashboard();
});

</script>

<template>
  <div v-if="isLoading" class="text-center p-5">
    <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
    <p class="mt-2 text-muted">Cargando dashboard...</p> </div>

  <div v-else-if="userData">
    <div class="dashboard-header mb-4">
        <h1 class="h3">Bienvenido, <span id="userName" class="text-primary-nb">{{ userData.nombre }}</span></h1>
        <p class="text-muted">Aqui tienes un resumen de tu actividad</p>
    </div>

    <div class="row g-4 mb-4">
        <div class="col-md-4">
            <div class="card p-3 card-shadow">
                <div class="d-flex align-items-center">
                    <div class="stat-icon bg-primary-nb rounded-3 p-3 text-white fs-4 me-3">
                        <i class="fas fa-child"></i>
                    </div>
                    <div>
                        <h3 id="totalHijos" class="h2 fw-bold mb-0">{{ userData.resumen?.total_hijos ?? 0 }}</h3>
                        <p class="text-muted mb-0">Hijos Registrados</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card p-3 card-shadow">
                <div class="d-flex align-items-center">
                    <div class="stat-icon bg-warning rounded-3 p-3 text-white fs-4 me-3">
                        <i class="fas fa-box"></i>
                    </div>
                    <div>
                        <h3 id="totalLoncheras" class="h2 fw-bold mb-0">{{ userData.resumen?.loncheras_este_mes ?? 0 }}</h3>
                        <p class="text-muted mb-0">Loncheras (este mes)</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card p-3 card-shadow">
                <div class="d-flex align-items-center">
                    <div class="stat-icon bg-info rounded-3 p-3 text-white fs-4 me-3">
                        <i class="fas fa-map-marker-alt"></i>
                    </div>
                    <div>
                        <h3 id="totalDirecciones" class="h2 fw-bold mb-0">{{ userData.resumen?.total_direcciones ?? 0 }}</h3>
                        <p class="text-muted mb-0">Direcciones</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row g-4">
        <div class="col-md-6">
            <div class="card p-4 card-shadow">
                <h5 class="mb-3 fw-bold">Acciones Rapidas</h5>
                <div class="d-grid gap-2">
                    <router-link to="/crear-lonchera" class="btn btn-primary-nb py-2">
                        <i class="fas fa-plus me-2"></i> Crear Nueva Lonchera
                    </router-link>
                    <router-link to="/hijos" class="btn btn-outline-primary py-2">
                        <i class="fas fa-child me-2"></i> Gestionar Hijos
                    </router-link>
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card p-4 card-shadow">
                <h5 class="mb-3 fw-bold">Informacion de Membresia</h5>
                <div class="d-flex justify-content-between mb-2">
                    <span class="fw-bold">Plan Actual:</span>
                    <span
                      v-if="userData.membresia"
                      :class="['badge', 'fs-6', getMembershipBadgeClass(userData.membresia.tipo)]"
                    >
                      {{ userData.membresia.tipo }}
                    </span>
                     <span v-else class="badge bg-secondary fs-6">N/A</span>
                </div>
                <div class="d-flex justify-content-between">
                    <span class="text-muted">Limite de Direcciones:</span>
                    <span id="maxDirecciones" v-if="userData.membresia">{{ userData.membresia.max_direcciones === 0 ? 'Ilimitado' : userData.membresia.max_direcciones }}</span>
                    <span id="maxDirecciones" v-else>N/A</span>
                </div>
                 <router-link to="/perfil" class="btn btn-sm btn-outline-secondary w-100 mt-4">
                        Ver detalles de membresia
                </router-link>
            </div>
        </div>
    </div>
  </div>

  <div v-else class="text-center p-5">
    <p class="text-danger">Error al cargar la informacion del usuario.</p>
    <p class="text-muted">Intenta <a href="/login" @click.prevent="forceLogout">iniciar sesión</a> de nuevo.</p>
  </div>

</template>

<style scoped>
/* Estilos específicos SOLO para el contenido del Dashboard */
/* Ya NO necesitas estilos para .sidebar aquí */
.stat-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>