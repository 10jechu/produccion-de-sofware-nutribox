<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { getUserDetail, hasRequiredMembership } from '@/utils/user';
import authService from '@/services/auth.service';

const router = useRouter();
const userData = ref(null);
const isLoading = ref(true);

// --- MODIFICADO: Renombrado para más claridad ---
const canSeeEstandarFeatures = computed(() => hasRequiredMembership('Estandar'));

const loadDashboard = async () => {
  isLoading.value = true;
  const user = getUserDetail();

  if (!user) {
    authService.logout();
    router.push('/login');
    return;
  }
  userData.value = user;
  isLoading.value = false;
};

const getMembershipBadgeClass = (tipo) => {
  if (tipo === 'Premium') {
    return 'bg-warning text-dark';
  } else if (tipo === 'Estandar') { 
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

      <div v-if="canSeeEstandarFeatures" class="row g-4 mb-4">
          <div class="col-md-4">
              <div class="card p-3 card-shadow">
                  <div class="d-flex align-items-center">
                      <div class="stat-icon bg-primary-nb rounded-3 p-3 text-white fs-4 me-3">
                          <i class="fas fa-child"></i>
                      </div>
                      <div>
                          <h3 id="totalHijos" class="h2 fw-bold mb-0">{{ userData.resumen?.total_hijos || 0 }}</h3>
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
                          <h3 id="totalLoncheras" class="h2 fw-bold mb-0">{{ userData.resumen?.loncheras_este_mes || 0 }}</h3>
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
                          <h3 id="totalDirecciones" class="h2 fw-bold mb-0">{{ userData.resumen?.total_direcciones || 0 }}</h3>
                          <p class="text-muted mb-0">Direcciones</p>
                      </div>
                  </div>
              </div>
          </div>
      </div>

      <div v-else class="row g-4 mb-4">
          <div class="col-12">
              <div class="card p-5 text-center card-shadow h-100">
                  <i class="fas fa-lock text-warning mb-3" style="font-size: 48px;"></i>
                  <h3 class="h4">Funciones de Plan Estándar o Premium</h3>
                  <p class="text-muted mb-4">
                      Para gestionar hijos, direcciones y crear loncheras, necesitas actualizar tu plan.
                      <br>¡Puedes empezar explorando nuestro recetario en la sección "Menús"!
                  </p>
                  <button class="btn btn-warning text-dark mx-auto" style="width: 200px;" disabled>Ver Planes</button>
              </div>
          </div>
      </div>

      <div class="row g-4">
          <div class="col-md-6">
              <div class="card p-4 card-shadow h-100">
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
                      <span>{{ userData.membresia ? userData.membresia.max_direcciones : '-' }}</span>
                  </div>
                   <router-link to="/perfil" class="btn btn-sm btn-outline-secondary w-100 mt-4">
                          Ver detalles de membresía
                  </router-link>
              </div>
          </div>
          
          <div class="col-md-6">
              <div v-if="canSeeEstandarFeatures" class="card p-4 card-shadow h-100">
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
              
              <div v-else class="card p-4 card-shadow h-100 text-center d-flex flex-column justify-content-center">
                  <i class="fas fa-book-open text-primary-nb mb-3" style="font-size: 48px;"></i>
                  <h5 class="mb-3 fw-bold">Explora los Menús</h5>
                  <p class="text-muted mb-4">
                      Tu plan "Free" te da acceso de lectura a todos nuestros menús predeterminados.
                  </p>
                  <router-link to="/menus" class="btn btn-primary-nb mt-auto">
                        <i class="fas fa-eye me-2"></i> Ver Menús (Recetario)
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
.stat-icon {
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
