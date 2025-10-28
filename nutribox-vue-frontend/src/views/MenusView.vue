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

const canAddMenu = computed(() => hasRequiredMembership('Estandar'));

async function loadMenus() {
    isLoading.value = true;
    userData.value = getUserDetail();
    if (!userData.value) {
        authService.logout();
        return;
    }

    if (!canAddMenu.value) {
        isLoading.value = false;
        return;
    }

    try {
        const allLunchboxes = await apiService.get('/lunchboxes');
        
        // Filtra y limita a 5, asumiendo que los menus son los que tienen hijo_id !== null
        menus.value = allLunchboxes.filter(lb => lb.hijo_id !== null).slice(0, 5);

        isLoading.value = false;
    } catch (error) {
        isLoading.value = false;
        Swal.fire('Error', error.message || 'No se pudieron cargar los menus.', 'error');
    }
}

async function addMenuToProfile(menuId) {
    try {
        Swal.showLoading();
        // SINTAXIS CORREGIDA: Concatenacion
        const originalMenu = await apiService.get('/lunchboxes/' + menuId + '/detail');
        
        const firstHijo = userData.value.hijos[0];
        if (!firstHijo) {
             Swal.close();
             Swal.fire('Advertencia', 'Debes tener al menos un hijo registrado para agregar un menu.', 'warning');
             return;
        }

        const newLunchbox = await apiService.post('/lunchboxes', {
            hijo_id: firstHijo.id,
            fecha: new Date().toISOString().split("T")[0],
            estado: "Borrador", 
            direccion_id: null 
        });

        for (const item of originalMenu.items) {
            await apiService.post('/lunchboxes/' + newLunchbox.id + '/items', {
                alimento_id: item.alimento_id,
                cantidad: item.cantidad
            });
        }
        
        Swal.close();
        Swal.fire('Exito', 'Menu agregado a Mis Loncheras como Borrador', 'success');
        
        setTimeout(() => {
             router.push('/mis-loncheras');
        }, 1500);

    } catch (error) {
        Swal.close();
        Swal.fire('Error', error.message || 'Error al agregar el menu a tu perfil.', 'error');
    }
}

onMounted(() => {
    loadMenus();
});

</script>

<template>
    <main class="flex-grow-1 p-4 bg-light">
        <div class="dashboard-header mb-4">
            <h1 class="h3">Menus Predeterminados</h1>
            <p class="text-muted">Explora nuestras loncheras recomendadas y agregalas a tu plan.</p>
        </div>

        <div v-if="!canAddMenu" class="card p-5 text-center card-shadow">
            <i class="fas fa-lock text-warning mb-3" style="font-size: 48px;"></i>
            <h3 class="h4">Funcion de Plan Estandar/Premium</h3>
            <p class="text-muted mb-4">Solo los planes Estandar y Premium pueden agregar menus a su perfil.</p>
        </div>

        <div v-else-if="isLoading" class="text-center p-5">
            <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
            <p class="mt-2 text-muted">Cargando menus...</p>
        </div>

        <div v-else-if="menus.length === 0" class="row g-4">
            <div class="col-12"><div class="card p-5 text-center card-shadow">No hay menus predeterminados disponibles en este momento.</div></div>
        </div>

        <div v-else id="menusContainer" class="row g-4">
            <div v-for="menu in menus" :key="menu.id" class="col-md-4">
                <div class="card h-100 card-shadow">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title fw-bold">Menu Recomendado #{{ menu.id }}</h5>
                        <p class="card-text text-muted">Una seleccion balanceada.</p>
                        <ul class="list-unstyled mt-3 mb-4">
                           <li><i class="fas fa-check text-success me-2"></i> Nutritivo y delicioso</li>
                           <li><i class="fas fa-check text-success me-2"></i> Aprobado por expertos</li>
                        </ul>
                        <div class="mt-auto">
                            <button class="btn btn-primary-nb w-100" @click="addMenuToProfile(menu.id)">
                                Agregar a Mis Loncheras
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>