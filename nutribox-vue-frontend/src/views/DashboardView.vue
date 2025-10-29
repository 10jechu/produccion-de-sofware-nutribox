<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router'; // Mantén esto si lo usas
import { getUserDetail } from '@/utils/user';
import authService from '@/services/auth.service'; // Mantén esto si lo usas

const router = useRouter(); // Asegúrate de que esto siga aquí si lo necesitas en el futuro
const userData = ref(null);
const isLoading = ref(true);

// LA FUNCIÓN logout YA NO VA AQUÍ, ESTÁ EN AppLayout.vue

const loadDashboard = async () => {
  isLoading.value = true;
  const user = getUserDetail();

  if (!user) {
    // Si no hay usuario, redirige a login (manejado por authService si es necesario)
    authService.logout(); // Esto ya redirige
    router.push('/login'); // Doble seguridad
    return;
  }
  userData.value = user;
  isLoading.value = false;
};

const getMembershipBadgeClass = (tipo) => {
  if (tipo === 'Premium') {
    return 'bg-warning text-dark';
  } else if (tipo === 'Estandar') { // Asegúrate de que coincida con el backend ('Estandar' o 'Estándar')
    return 'bg-info';
  } else {
    return 'bg-secondary';
  }
};

onMounted(() => {
  loadDashboard();
});

</script>

<template>
  <main class="flex-grow-1 p-4 bg-light">
    <div v-if="isLoading" class="text-center p-5">
      <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
      <p class="mt-2 text-muted">Cargando dashboard...</p>
    </div>

    <div v-else-if="userData">
      <div class="dashboard-header mb-4">
          <h1 class="h3">Bienvenido, <span class="text-primary-nb">{{ userData.nombre }}</span></h1>
          <p class="text-muted">Aquí tienes un resumen de tu actividad</p>
      </div>

      <div class="row g-4 mb-4">
          <div class="col-md-4">
              <div class="card p-3 card-shadow">
                  <div class="d-flex align-items-center">
                      <div class="stat-icon bg-primary-nb rounded-3 p-3 text-white fs-4 me-3">
                          <i class="fas fa-child"></i>
                      </div>
                      <div>
                          <h3 class="h2 fw-bold mb-0">{{ userData.resumen?.total_hijos || 0 }}</h3>
                          <p class="text-muted mb-0">Hijos Registrados</p>
                      </div>
                  </div>
              </div>
          </div>
          <div class="col-md-4">
              <div class="card p-3 card-shadow">
                  <div class="d-flex align-items-center">
                      <div class="stat-icon bg-warning rounded-3 p-3 text-dark fs-4 me-3">
                          <i class="fas fa-box"></i>
                      </div>
                      <div>
                          <h3 class="h2 fw-bold mb-0">{{ userData.resumen?.loncheras_este_mes || 0 }}</h3>
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
                          <h3 class="h2 fw-bold mb-0">{{ userData.resumen?.total_direcciones || 0 }}</h3>
                          <p class="text-muted mb-0">Direcciones</p>
                      </div>
                  </div>
              </div>
          </div>
      </div>

      <div class="row g-4">
          <div class="col-md-6">
              <div class="card p-4 card-shadow">
                  <h5 class="mb-3 fw-bold">Acciones Rápidas</h5>
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
                  <h5 class="mb-3 fw-bold">Información de Membresía</h5>
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
                      <span class="text-muted">Límite de Direcciones:</span>
                      <span>{{ userData.membresia ? (userData.membresia.max_direcciones === 0 ? 'Ilimitado' : userData.membresia.max_direcciones) : '-' }}</span>
                  </div>
                   <router-link to="/perfil" class="btn btn-sm btn-outline-secondary w-100 mt-4">
                          Ver detalles de membresía
                  </router-link>
              </div>
          </div>
      </div>
    </div>

    <div v-else class="text-center p-5">
      <p class="text-danger">Error al cargar la información del usuario.</p>
    </div>
  </main>
</template>

<style scoped>
/* Los estilos específicos del sidebar se BORRARON. Se usan los globales de main.css */
.stat-icon {
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
