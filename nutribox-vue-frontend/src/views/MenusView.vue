<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { getUserDetail, hasRequiredMembership } from '@/utils/user';
import authService from '@/services/auth.service';
import { useRouter } from 'vue-router';

const router = useRouter();
const menus = ref([]);
const userData = ref(null);
const isLoading = ref(true);

// ### INICIO DE LA MODIFICACIÓN ###
// Básico ('Free') puede ver la página
const canAccessPage = computed(() => hasRequiredMembership('Free')); 
// Estándar puede usar el botón "Agregar"
const canAddMenu = computed(() => hasRequiredMembership('Estandar'));
// ### FIN DE LA MODIFICACIÓN ###

function formatCurrency(value) {
    const numberValue = Number(value);
    if (isNaN(numberValue)) return '$ 0';
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(numberValue);
}

async function loadMenus() {
    isLoading.value = true;
    userData.value = getUserDetail();
    if (!userData.value) { authService.logout(); return; }
    
    // No bloquees la carga si no es estándar, solo el botón
    if (!canAccessPage.value) { isLoading.value = false; return; }

    try {
        const detailedMenus = await apiService.get('/menus-predeterminados');
        menus.value = detailedMenus;
        isLoading.value = false;
    } catch (error) {
        isLoading.value = false;
        Swal.fire('Error', error.message || 'No se pudieron cargar los menús predeterminados.', 'error');
    }
}

async function addMenuToProfile(menuDetail) {
     // Esta validación ya está correcta, comprueba 'Estandar'
     if (!canAddMenu.value) {
         Swal.fire('Función Estándar', 'Necesitas un plan Estándar o Premium para agregar menús a tu perfil.', 'info');
         return;
     }

     if (!menuDetail || !menuDetail.items || menuDetail.items.length === 0) {
        Swal.fire('Error', 'El menú seleccionado está vacío o es inválido.', 'warning');
        return;
     }
     const userHijos = userData.value?.hijos || [];
     if (userHijos.length === 0) {
         Swal.fire('Advertencia', 'Debes tener al menos un hijo registrado para agregar un menú.', 'warning');
         router.push('/hijos');
         return;
     }
     const targetHijoId = userHijos[0].id; 
     try {
         Swal.fire({ title: 'Agregando menú...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });
         const newLunchbox = await apiService.post('/lunchboxes', {
             hijo_id: targetHijoId,
             fecha: new Date().toISOString().split("T")[0],
             estado: "Borrador",
             direccion_id: null,
             es_predeterminada: false 
         });
         for (const item of menuDetail.items) {
             await apiService.post('/lunchboxes/' + newLunchbox.id + '/items', {
                 alimento_id: item.alimento_id, 
                 cantidad: item.cantidad
             });
         }
         Swal.close();
         Swal.fire('¡Éxito!', 'Menú agregado a "Mis Loncheras" como Borrador.', 'success');
         setTimeout(() => { router.push('/mis-loncheras'); }, 1500);
     } catch (error) {
         Swal.close();
         Swal.fire('Error', error.message || 'Error al agregar el menú a tu perfil.', 'error');
     }
}

onMounted(() => {
    loadMenus();
});

</script>

<template>
    <main class="flex-grow-1 p-4 bg-light">
        <div class="dashboard-header mb-4">
            <h1 class="h3">Menús Predeterminados</h1>
            <p class="text-muted">Explora nuestras loncheras recomendadas y agrégalas a tu plan.</p>
        </div>

        <div v-if="!canAccessPage" class="card p-5 text-center card-shadow">
            <i class="fas fa-lock text-warning mb-3" style="font-size: 48px;"></i>
            <h3 class="h4">Función Bloqueada</h3>
            <p class="text-muted mb-4">Esta función no está disponible para tu plan actual.</p>
        </div>

        <div v-else-if="isLoading" class="text-center p-5">
            <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
            <p class="mt-2 text-muted">Cargando menús...</p>
        </div>

        <div v-else-if="menus.length === 0" class="row g-4">
            <div class="col-12">
                <div class="card p-5 text-center card-shadow">
                    <i class="fas fa-info-circle text-muted mb-3 fs-1"></i>
                    <h4 class="h5">Aún no hay menús predeterminados</h4>
                    <p class="text-muted">Pronto añadiremos nuevas recomendaciones.</p>
                </div>
            </div>
        </div>

        <div v-else id="menusContainer" class="row g-4">
            <div v-for="menu in menus" :key="menu.id" class="col-md-4">
                <div class="card h-100 card-shadow">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title fw-bold">{{ menu.nombre }}</h5>
                        <p class="card-text text-muted small">
                            {{ menu.items.length }} items |
                            {{ menu.nutricion_total?.calorias?.toFixed(0) || 0 }} kcal |
                            {{ formatCurrency(menu.costo_total || 0) }}
                        </p>
                        <ul class="list-unstyled mt-2 mb-3 small">
                           <li v-for="item in menu.items.slice(0, 3)" :key="item.alimento_id">
                                <i class="fas fa-check text-success me-1"></i>
                                {{ item.alimento?.nombre || `ID ${item.alimento_id}` }} ({{ item.cantidad }}x)
                           </li>
                           <li v-if="menu.items.length > 3" class="text-muted">... y más</li>
                        </ul>
                        <div class="mt-auto">
                            <button 
                                :class="['btn', 'w-100', canAddMenu ? 'btn-primary-nb' : 'btn-secondary']" 
                                @click="addMenuToProfile(menu)"
                                :disabled="!canAddMenu"
                                :title="canAddMenu ? 'Agregar a Mis Loncheras' : 'Requiere Plan Estándar o Premium'"
                            >
                                {{ canAddMenu ? 'Agregar a Mis Loncheras' : 'Requiere Estándar' }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped>
.card-body ul li { line-height: 1.4; }
</style>
