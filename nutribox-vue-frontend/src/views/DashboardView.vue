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

// Función auxiliar para clases de badge (Premium Amarillo, Estandar Verde, etc.)
const getMembershipBadgeClass = (tipo) => {
  if (tipo === 'Premium') {
    return 'bg-secondary text-dark-nb'; // Amarillo miel
  } else if (tipo === 'Estandar') { 
    return 'bg-primary-dark text-white'; // Verde oscuro
  } else { 
    return 'bg-secondary text-dark-nb';
  }
};

onMounted(() => {
  loadDashboard();
});

</script>

<template>
  <main class="flex-grow-1 p-4 bg-light-nb">
    <div v-if="isLoading" class="text-center p-5 bg-light-nb">
      <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
      <p class="mt-2 text-muted-dark">Cargando dashboard...</p> </div>

    <div v-else-if="userData">
        <div class="dashboard-header mb-4">
            <h1 class="h3 text-dark-nb">Bienvenido, <span id="userName" class="text-primary-nb">{{ userData.nombre }}</span></h1>
            <p class="text-muted-dark">Aquí tienes un resumen de tu actividad</p>
        </div>

        <div class="row g-4 mb-4">
            <div class="col-md-4">
                <router-link to="/app/hijos" class="stat-card-link text-decoration-none">
                    <div class="card p-4 card-shadow-top h-100">
                        <div class="d-flex align-items-center justify-content-between">
                            <div>
                                <h3 id="totalHijos" class="h2 fw-bold mb-0 text-dark-nb">{{ userData.resumen?.total_hijos ?? 0 }}</h3>
                                <p class="text-muted-dark mb-1 small">Hijos Registrados</p>
                            </div>
                            <div class="stat-icon bg-primary-light text-white">
                                <i class="fas fa-child"></i>
                            </div>
                        </div>
                    </div>
                </router-link>
            </div>
            <div class="col-md-4">
                <router-link to="/app/mis-loncheras" class="stat-card-link text-decoration-none">
                    <div class="card p-4 card-shadow-top h-100">
                        <div class="d-flex align-items-center justify-content-between">
                            <div>
                                <h3 id="totalLoncheras" class="h2 fw-bold mb-0 text-dark-nb">{{ userData.resumen?.loncheras_este_mes ?? 0 }}</h3>
                                <p class="text-muted-dark mb-1 small">Loncheras (este mes)</p>
                            </div>
                            <div class="stat-icon bg-secondary text-dark-nb">
                                <i class="fas fa-box"></i>
                            </div>
                        </div>
                    </div>
                </router-link>
            </div>
            <div class="col-md-4">
                <router-link to="/app/direcciones" class="stat-card-link text-decoration-none">
                    <div class="card p-4 card-shadow-top h-100">
                        <div class="d-flex align-items-center justify-content-between">
                            <div>
                                 <h3 id="totalDirecciones" class="h2 fw-bold mb-0 text-dark-nb">{{ userData.resumen?.total_direcciones ?? 0 }}</h3>
                                 <p class="text-muted-dark mb-1 small">Direcciones</p>
                            </div>
                            <div class="stat-icon bg-accent text-white">
                                <i class="fas fa-map-marker-alt"></i>
                            </div>
                        </div>
                    </div>
                </router-link>
            </div>
        </div>
        <div class="row g-4">
            <div class="col-lg-6">
                <div class="card p-4 card-shadow h-100">
                    <h5 class="mb-3 fw-bold text-dark-nb">Acciones Rápidas</h5>
                    <div class="d-grid gap-3">
                        <router-link to="/app/crear-lonchera" class="btn btn-primary-nb py-3">
                            <i class="fas fa-plus me-2"></i> Crear Nueva Lonchera
                        </router-link>
                        <router-link to="/app/hijos" class="btn btn-outline-primary-nb py-3">
                            <i class="fas fa-child me-2"></i> Gestionar Hijos
                        </router-link>
                        
                        <router-link v-if="userData.rol.nombre === 'Admin'" to="/app/admin/foods" class="btn btn-primary-dark py-3 mt-3">
                             <i class="fas fa-cog me-2"></i> Panel de Administración
                        </router-link>
                    </div>
                </div>
            </div>

            <div class="col-lg-6">
                <div class="card p-4 card-shadow h-100">
                    <h5 class="mb-3 fw-bold text-dark-nb">Información de Membresía</h5>
                    <div class="d-flex justify-content-between py-2 border-bottom">
                        <span class="fw-bold text-dark-nb">Plan Actual:</span>
                        <span
                          v-if="userData.membresia"
                          :class="['badge', 'fs-6', getMembershipBadgeClass(userData.membresia.tipo)]"
                        >
                          {{ userData.membresia.tipo }}
                        </span>
                         <span v-else class="badge bg-muted-dark fs-6">N/A</span>
                    </div>
                    <div class="d-flex justify-content-between py-2">
                        <span class="text-muted-dark">Límite de Direcciones:</span>
                        <span id="maxDirecciones" v-if="userData.membresia" class="text-dark-nb">{{ userData.membresia.max_direcciones === 0 ? 'Ilimitado' : userData.membresia.max_direcciones }}</span>
                        <span id="maxDirecciones" v-else class="text-dark-nb">N/A</span>
                    </div>
                     <router-link to="/app/perfil" class="btn btn-sm btn-outline-primary-nb w-100 mt-4">
                            Ver detalles de membresía
                    </router-link>
                </div>
            </div>
        </div>
      </div>

    <div v-else class="text-center p-5 bg-light-nb">
      <p class="text-danger">Error al cargar la información del usuario.</p>
      <p class="text-muted-dark">Intenta <router-link to="/login">iniciar sesión</router-link> de nuevo.</p>
    </div>
  </main>
</template>

<style scoped>
/* Estilos específicos para el componente */
.stat-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.2rem; 
  border-radius: 50%;
}
.stat-card-link {
    display: block;
    text-decoration: none;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.stat-card-link:hover .card {
    transform: translateY(-5px); 
    box-shadow: var(--shadow-xl);
    cursor: pointer;
}

/* Para mantener la estética limpia como la imagen de referencia */
.card-shadow-top {
    box-shadow: var(--shadow-md); 
    border: 1px solid var(--nb-border-medium);
    background-color: var(--bg-card); 
    border-radius: 0.75rem; 
}
.card-shadow-top:hover {
     box-shadow: var(--shadow-lg); 
}
</style>
