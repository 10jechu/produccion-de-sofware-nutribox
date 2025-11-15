<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
// --- MODIFICADO: Añadido 'isAdmin' ---
import { getUserDetail, hasRequiredMembership, isAdmin } from '@/utils/user'; 
import authService from '@/services/auth.service';
import { useRouter } from 'vue-router';

const userData = ref(null);
const isLoading = ref(true);
const router = useRouter();

const canSeeSummary = computed(() => hasRequiredMembership('Estandar'));
// --- AÑADIDO: Computada para saber si es Admin ---
const isUserAdmin = computed(() => isAdmin());

const getMembershipBadgeClass = (tipo) => {
    if (tipo === 'Premium') {
        return 'bg-warning text-dark';
    } else if (tipo === 'Estandar') { 
        return 'bg-info';
    } else {
        return 'bg-secondary';
    }
};

const loadProfile = async () => {
    isLoading.value = true;
    const user = getUserDetail();
    if (!user) {
        authService.logout();
        return;
    }
    
    try {
        const freshDetail = await apiService.get('/users/' + user.id + '/detail');
        authService.saveUserDetail(freshDetail); 
        userData.value = freshDetail;
        isLoading.value = false;
    } catch (error) {
        isLoading.value = false;
        Swal.fire('Error', error.message || 'No se pudo cargar el perfil', 'error');
        authService.logout();
    }
};

const showEditProfileModal = () => {
    Swal.fire("Funcion No Implementada", "La edicion de perfil esta pendiente.", "info");
}

onMounted(() => {
    loadProfile();
});
</script>

<template>
    <main class="flex-grow-1 p-4 bg-light">
        <div class="dashboard-header mb-4">
            <h1 class="h3">Mi Perfil</h1>
            <p class="text-muted">Visualiza y gestiona las opciones de tu cuenta.</p>
        </div>

        <div v-if="isLoading" class="text-center p-5">
            <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
            <p class="mt-2">Cargando perfil...</p>
        </div>

        <div v-else-if="userData" class="row g-4">
            <div :class="isUserAdmin ? 'col-lg-12' : 'col-lg-6'">
            <div class="card p-4 card-shadow h-100">
                    <h5 class="card-title fw-bold mb-3">Informacion Personal y Cuenta</h5>
                    <div class="text-center mb-4">
                        <div class="rounded-circle bg-light d-inline-block p-4 mb-3">
                            <i class="fas fa-user-circle text-primary-nb" style="font-size: 64px;"></i>
                        </div>
                        <h4 id="userName" class="fw-bold">{{ userData.nombre }}</h4>
                        <p id="userEmail" class="text-muted mb-0">{{ userData.email }}</p>
                    </div>
                    <p><strong>Rol:</strong> <span class="badge bg-info">{{ userData.rol.nombre }}</span></p>
                    <p>
                        <strong>Membresia:</strong> 
                        <span :class="['badge', getMembershipBadgeClass(userData.membresia.tipo)]">{{ userData.membresia.tipo }}</span>
                    </p>
                    
                    <button class="btn btn-outline-primary w-100 mt-3" @click="showEditProfileModal">
                        <i class="fas fa-edit me-1"></i> Editar Nombre/Email
                    </button>
                </div>
            </div>
            
            <div v-if="!isUserAdmin" class="col-lg-6">
            <div v-if="canSeeSummary" class="card p-4 card-shadow h-100">
                    <h5 class="card-title fw-bold mb-3">Resumen y Direcciones</h5>
                    <div class="d-flex justify-content-between py-2 border-bottom">
                        <span>Total Hijos:</span>
                        <strong id="totalHijos">{{ userData.resumen.total_hijos }}</strong>
                    </div>
                    <div class="d-flex justify-content-between py-2 border-bottom">
                        <span>Direcciones Registradas:</span>
                        <strong id="totalDirecciones">{{ userData.resumen.total_direcciones }} / {{ userData.membresia.max_direcciones === 0 ? 'Ilimitado' : userData.membresia.max_direcciones }}</strong>
                    </div>

                    <router-link to="/direcciones" class="btn btn-sm btn-primary-nb w-100 mt-4">
                        Gestionar Direcciones
                    </router-link>
                </div>

                <div v-else class="card p-5 text-center card-shadow h-100">
                     <i class="fas fa-lock text-warning mb-3" style="font-size: 48px;"></i>
                     <h3 class="h4">Función de Plan Estándar</h3>
                     <p class="text-muted mb-4">
                         La gestión de hijos y direcciones está disponible en los planes Estándar y Premium.
                     </p>
                     <button class="btn btn-warning text-dark" disabled>Ver Planes</button>
                </div>
            </div>
            </div>
    </main>
</template>

<style scoped>
/* Los estilos de Bootstrap y main.css manejan la apariencia */
</style>
