<template>
  <div class="dashboard-container">
    <!-- Header del Dashboard -->
    <div class="dashboard-header mb-4">
      <h1 class="h2 mb-2">Dashboard</h1>
      <p class="text-muted">Bienvenido a tu panel de control de NutriBox</p>
    </div>

    <!-- Tarjeta de Información del Usuario -->
    <div class="row">
      <div class="col-lg-8">
        <div class="card shadow-sm mb-4">
          <div class="card-header bg-success text-white">
            <h5 class="card-title mb-0">
              <i class="fas fa-user-circle me-2"></i>Información de tu Cuenta
            </h5>
          </div>
          <div class="card-body">
            <div v-if="isLoading" class="text-center py-4">
              <div class="spinner-border text-success" role="status">
                <span class="visually-hidden">Cargando...</span>
              </div>
              <p class="mt-2 text-muted">Cargando información...</p>
            </div>

            <div v-else-if="userData" class="user-info">
              <div class="row">
                <div class="col-md-6">
                  <div class="info-item mb-3">
                    <label class="form-label text-muted mb-1">Nombre</label>
                    <p class="fs-5 mb-0">{{ userData.nombre || 'No especificado' }}</p>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-item mb-3">
                    <label class="form-label text-muted mb-1">Email</label>
                    <p class="fs-6 mb-0">{{ userData.email || 'No especificado' }}</p>
                  </div>
                </div>
              </div>

              <div class="row">
                <div class="col-md-6">
                  <div class="info-item mb-3">
                    <label class="form-label text-muted mb-1">Rol</label>
                    <div>
                      <span :class="getRoleBadgeClass(userData.rol?.nombre)" class="badge fs-6">
                        {{ userData.rol?.nombre || 'Usuario' }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-item mb-3">
                    <label class="form-label text-muted mb-1">Plan de Membresía</label>
                    <div>
                      <span :class="getMembershipBadgeClass(userData.membresia?.tipo)" class="badge fs-6">
                        {{ userData.membresia?.tipo || 'Free' }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Información específica por Rol -->
              <div v-if="userData.rol?.nombre === 'Admin'" class="admin-info mt-4 p-3 bg-light rounded">
                <h6 class="text-success mb-3">
                  <i class="fas fa-shield-alt me-2"></i>Privilegios de Administrador
                </h6>
                <ul class="list-unstyled mb-0">
                  <li><i class="fas fa-check text-success me-2"></i>Gestionar alimentos del sistema</li>
                  <li><i class="fas fa-check text-success me-2"></i>Crear y editar menús base</li>
                  <li><i class="fas fa-check text-success me-2"></i>Acceso al panel de administración</li>
                  <li><i class="fas fa-check text-success me-2"></i>Ver todos los usuarios registrados</li>
                </ul>
              </div>

              <!-- Información de Membresía para Usuarios Normales -->
              <div v-else class="membership-info mt-4">
                <h6 class="text-primary mb-3">
                  <i class="fas fa-crown me-2"></i>Beneficios de tu Plan
                </h6>
                <div class="row">
                  <div class="col-md-6" v-if="userData.membresia?.tipo === 'Free'">
                    <ul class="list-unstyled">
                      <li><i class="fas fa-eye text-success me-2"></i>Visualizar alimentos</li>
                      <li><i class="fas fa-book-open text-success me-2"></i>Ver menús predeterminados</li>
                      <li><i class="fas fa-info-circle text-warning me-2"></i>Solo visualización</li>
                    </ul>
                    <div class="mt-3 p-3 bg-warning bg-opacity-10 rounded">
                      <small class="text-warning">
                        <i class="fas fa-lightbulb me-1"></i>
                        Actualiza tu plan para crear loncheras personalizadas
                      </small>
                    </div>
                  </div>
                  <div class="col-md-6" v-else-if="userData.membresia?.tipo === 'Estandar'">
                    <ul class="list-unstyled">
                      <li><i class="fas fa-plus-circle text-success me-2"></i>Crear loncheras</li>
                      <li><i class="fas fa-copy text-success me-2"></i>Copiar menús predeterminados</li>
                      <li><i class="fas fa-map-marker-alt text-success me-2"></i>1 dirección de entrega</li>
                    </ul>
                  </div>
                  <div class="col-md-6" v-else-if="userData.membresia?.tipo === 'Premium'">
                    <ul class="list-unstyled">
                      <li><i class="fas fa-star text-warning me-2"></i>Todas las funciones Estándar</li>
                      <li><i class="fas fa-map-marker-alt text-warning me-2"></i>Hasta 3 direcciones</li>
                      <li><i class="fas fa-history text-warning me-2"></i>Historial de consumo</li>
                      <li><i class="fas fa-shield-alt text-warning me-2"></i>Restricciones alimentarias</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Panel de Acciones Rápidas -->
      <div class="col-lg-4">
        <div class="card shadow-sm mb-4">
          <div class="card-header bg-primary text-white">
            <h5 class="card-title mb-0">
              <i class="fas fa-bolt me-2"></i>Acciones Rápidas
            </h5>
          </div>
          <div class="card-body">
            <div class="d-grid gap-2">
              <!-- Para Admin -->
              <template v-if="userData?.rol?.nombre === 'Admin'">
                <router-link to="/app/alimentos" class="btn btn-success">
                  <i class="fas fa-utensils me-2"></i>Gestionar Alimentos
                </router-link>
                
                <router-link to="/app/menus" class="btn btn-outline-success">
                  <i class="fas fa-book-open me-2"></i>Gestionar Menús
                </router-link>

                <router-link to="/app/admin/foods" class="btn btn-warning">
                  <i class="fas fa-cog me-2"></i>Panel de Administración
                </router-link>
              </template>

              <!-- Para Usuarios Normales -->
              <template v-else>
                <router-link 
                  to="/app/crear-lonchera" 
                  class="btn btn-success"
                  v-if="userData?.membresia?.tipo !== 'Free'"
                >
                  <i class="fas fa-plus-circle me-2"></i>Crear Lonchera
                </router-link>

                <router-link 
                  to="/app/crear-lonchera" 
                  class="btn btn-outline-warning"
                  v-else
                >
                  <i class="fas fa-crown me-2"></i>Actualizar Plan para Crear
                </router-link>
                
                <router-link to="/app/alimentos" class="btn btn-outline-success">
                  <i class="fas fa-utensils me-2"></i>Ver Alimentos
                </router-link>

                <router-link to="/app/menus" class="btn btn-outline-primary">
                  <i class="fas fa-book-open me-2"></i>Explorar Menús
                </router-link>
              </template>

              <router-link to="/app/perfil" class="btn btn-outline-info">
                <i class="fas fa-user-edit me-2"></i>Editar Perfil
              </router-link>

              <router-link 
                to="/app/perfil" 
                class="btn btn-warning"
                v-if="userData?.membresia?.tipo === 'Free' && userData?.rol?.nombre !== 'Admin'"
              >
                <i class="fas fa-rocket me-2"></i>Mejorar Plan
              </router-link>
            </div>
          </div>
        </div>

        <!-- Tarjeta de Estadísticas -->
        <div class="card shadow-sm">
          <div class="card-header bg-info text-white">
            <h5 class="card-title mb-0">
              <i class="fas fa-chart-pie me-2"></i>Resumen
            </h5>
          </div>
          <div class="card-body">
            <div class="text-center">
              <div class="mb-3" v-if="userData?.rol?.nombre !== 'Admin'">
                <i class="fas fa-user-friends fa-2x text-info mb-2"></i>
                <h4 class="mb-0">{{ userData?.hijos?.length || 0 }}</h4>
                <small class="text-muted">Hijos registrados</small>
              </div>
              <div class="mb-3" v-if="userData?.rol?.nombre !== 'Admin'">
                <i class="fas fa-utensils fa-2x text-success mb-2"></i>
                <h4 class="mb-0">{{ userData?.resumen?.total_loncheras || 0 }}</h4>
                <small class="text-muted">Loncheras creadas</small>
              </div>
              <div class="mb-3" v-if="userData?.rol?.nombre === 'Admin'">
                <i class="fas fa-utensils fa-2x text-primary mb-2"></i>
                <h4 class="mb-0">Administrador</h4>
                <small class="text-muted">Panel de control</small>
              </div>
              <div v-if="userData?.membresia?.tipo === 'Free' && userData?.rol?.nombre !== 'Admin'" class="mt-3 p-2 bg-light rounded">
                <small class="text-muted">
                  <i class="fas fa-info-circle me-1"></i>
                  Actualiza tu plan para desbloquear todas las funciones
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getUserDetail } from '@/utils/user';
import { useRouter } from 'vue-router';
import authService from '@/services/auth.service';

const userData = ref(null);
const isLoading = ref(true);
const router = useRouter();

const loadDashboard = async () => {
  isLoading.value = true;
  const user = getUserDetail();

  if (!user) {
    authService.logout();
    router.push('/login');
    isLoading.value = false;
    return;
  }

  userData.value = user;
  isLoading.value = false;
};

// Clases para badges de rol
const getRoleBadgeClass = (rol) => {
  if (rol === 'Admin') {
    return 'bg-warning text-dark';
  }
  return 'bg-secondary text-white';
};

// Clases para badges de membresía
const getMembershipBadgeClass = (tipo) => {
  if (tipo === 'Premium') {
    return 'bg-warning text-dark';
  } else if (tipo === 'Estandar') {
    return 'bg-success text-white';
  } else {
    return 'bg-secondary text-white';
  }
};

onMounted(() => {
  loadDashboard();
});
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 1rem;
}

.user-info .info-item label {
  font-size: 0.875rem;
  font-weight: 500;
}

.badge {
  padding: 0.5em 0.75em;
}

.card {
  border: none;
  border-radius: 10px;
}

.card-header {
  border-radius: 10px 10px 0 0 !important;
  font-weight: 600;
}

.btn {
  border-radius: 8px;
  font-weight: 500;
}

.admin-info, .membership-info {
  border-left: 4px solid #1F8D45;
}

.list-unstyled li {
  padding: 0.25rem 0;
}
</style>