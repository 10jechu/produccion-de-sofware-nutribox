<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getUserDetail } from '@/utils/user';
import authService from '@/services/auth.service';

const router = useRouter();
const userData = ref(null);
const isLoading = ref(true);

const logout = () => {
  authService.logout();
  router.push('/login');
};

const loadDashboard = async () => {
  isLoading.value = true;
  const user = getUserDetail();
  
  if (!user) {
    logout();
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
  <div class="d-flex" style="min-height: 100vh;">
    <aside class="sidebar bg-white shadow-sm p-4 d-flex flex-column" style="width: 260px;">
        <div class="sidebar-logo mb-4 fs-4 fw-bold text-primary-nb">?? NutriBox</div>
        <nav class="nav nav-pills flex-column sidebar-nav">
            <router-link to="/dashboard" class="nav-link text-dark" active-class="active"><i class="fas fa-home fa-fw me-2"></i> Dashboard</router-link>
            <router-link to="/hijos" class="nav-link text-dark"><i class="fas fa-child fa-fw me-2"></i> Mis Hijos</router-link>
            <router-link to="/crear-lonchera" class="nav-link text-dark"><i class="fas fa-plus-circle fa-fw me-2"></i> Crear Lonchera</router-link>
            <router-link to="/mis-loncheras" class="nav-link text-dark"><i class="fas fa-list fa-fw me-2"></i> Mis Loncheras</router-link>
            <router-link to="/direcciones" class="nav-link text-dark"><i class="fas fa-map-marker-alt fa-fw me-2"></i> Direcciones</router-link>
            <router-link to="/restricciones" class="nav-link text-dark"><i class="fas fa-ban fa-fw me-2"></i> Restricciones</router-link>
            <router-link to="/alimentos" class="nav-link text-dark"><i class="fas fa-utensils fa-fw me-2"></i> Alimentos</router-link>
            <router-link to="/menus" class="nav-link text-dark"><i class="fas fa-book-open fa-fw me-2"></i> Menus</router-link>
            <router-link to="/estadisticas" class="nav-link text-dark"><i class="fas fa-chart-line fa-fw me-2"></i> Estadisticas</router-link>
            <router-link to="/perfil" class="nav-link text-dark"><i class="fas fa-user-circle fa-fw me-2"></i> Mi Perfil</router-link>
            
            <router-link v-if="userData && userData.rol.nombre === 'Admin'" to="/admin/foods" class="nav-link text-dark mt-3">
                <i class="fas fa-cog fa-fw me-2"></i> Admin Panel
            </router-link>
            
            <a class="nav-link mt-auto" href="#" @click.prevent="logout"><i class="fas fa-sign-out-alt fa-fw me-2"></i> Cerrar Sesion</a>
        </nav>
    </aside>

    <main class="flex-grow-1 p-4 bg-light">
      <div v-if="isLoading" class="text-center p-5">
        <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
        <p class="mt-2">Cargando dashboard...</p>
      </div>

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
                            <h3 id="totalHijos" class="h2 fw-bold mb-0">{{ userData.resumen.total_hijos }}</h3>
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
                            <h3 id="totalLoncheras" class="h2 fw-bold mb-0">{{ userData.resumen.loncheras_este_mes }}</h3>
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
                            <h3 id="totalDirecciones" class="h2 fw-bold mb-0">{{ userData.resumen.total_direcciones }}</h3>
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
                          :class="['badge', 'fs-6', getMembershipBadgeClass(userData.membresia.tipo)]"
                        >
                          {{ userData.membresia.tipo }}
                        </span>
                    </div>
                    <div class="d-flex justify-content-between">
                        <span class="text-muted">Limite de Direcciones:</span>
                        <span id="maxDirecciones">{{ userData.membresia.max_direcciones === 0 ? 'Ilimitado' : userData.membresia.max_direcciones }}</span>
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
      </div>
    </main>
  </div>
</template>

<style scoped>
.sidebar { height: 100vh; }
.nav-link.router-link-active, .nav-link.active { background-color: var(--primary) !important; color: white !important; }
</style>
