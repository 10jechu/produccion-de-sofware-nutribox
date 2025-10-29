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

// Permiso para ver/agregar menús (Estándar o superior)
const canAccessMenus = computed(() => hasRequiredMembership('Estandar'));

// Función para formatear moneda
function formatCurrency(value) {
    const numberValue = Number(value);
    if (isNaN(numberValue)) return '$ 0';
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(numberValue);
}

// Carga solo menús predeterminados
async function loadMenus() {
    isLoading.value = true;
    userData.value = getUserDetail();
    if (!userData.value) {
        authService.logout();
        return;
    }

    // Si no tiene plan Estándar o superior, no cargar nada
    if (!canAccessMenus.value) {
        isLoading.value = false;
        return;
    }

    try {
        // Pide al backend SOLO las loncheras marcadas como predeterminadas
        const predeterminedMenus = await apiService.get('/lunchboxes?es_predeterminada=true');

        // Para mostrar info útil, obtenemos el detalle de cada menú
        const detailedMenusPromises = predeterminedMenus.map(menu =>
            apiService.get('/lunchboxes/' + menu.id + '/detail') // Usamos concatenación
        );
        const detailedMenus = await Promise.all(detailedMenusPromises);

        menus.value = detailedMenus; // Guardamos los menús detallados
        isLoading.value = false;
    } catch (error) {
        isLoading.value = false;
        Swal.fire('Error', error.message || 'No se pudieron cargar los menús predeterminados.', 'error');
    }
}

// Agrega un menú predeterminado al perfil del usuario actual (como Borrador)
async function addMenuToProfile(menuDetail) {
    if (!menuDetail || !menuDetail.items || menuDetail.items.length === 0) {
        Swal.fire('Error', 'El menú seleccionado está vacío o es inválido.', 'warning');
        return;
    }

    // Necesita tener al menos un hijo registrado
    const userHijos = userData.value?.hijos || [];
    if (userHijos.length === 0) {
         Swal.fire('Advertencia', 'Debes tener al menos un hijo registrado para agregar un menú.', 'warning');
         router.push('/hijos'); // Sugerir ir a registrar hijos
         return;
    }
    // Asignamos al primer hijo por defecto (o podríamos preguntar)
    const targetHijoId = userHijos[0].id;

    try {
        Swal.fire({ title: 'Agregando menú...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });

        // 1. Crear una nueva lonchera 'Borrador' para el hijo del usuario
        const newLunchbox = await apiService.post('/lunchboxes', {
            hijo_id: targetHijoId,
            fecha: new Date().toISOString().split("T")[0], // Fecha de hoy
            estado: "Borrador",
            direccion_id: null,
            // Importante: NO marcarla como predeterminada
            es_predeterminada: false
        });

        // 2. Copiar los items del menú predeterminado a la nueva lonchera
        for (const item of menuDetail.items) {
            await apiService.post('/lunchboxes/' + newLunchbox.id + '/items', { // Usamos concatenación
                alimento_id: item.alimento_id,
                cantidad: item.cantidad
            });
        }

        Swal.close();
        Swal.fire('¡Éxito!', 'Menú agregado a "Mis Loncheras" como Borrador.', 'success');

        // Redirigir a Mis Loncheras para que el usuario vea/confirme
        setTimeout(() => {
             router.push('/mis-loncheras');
        }, 1500);

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




        <div v-if="!canAccessMenus" class="card p-5 text-center card-shadow">
            <i class="fas fa-lock text-warning mb-3" style="font-size: 48px;"></i>
            <h3 class="h4">Función de Plan Estándar/Premium</h3>
            <p class="text-muted mb-4">Solo los planes Estándar y Premium pueden explorar y agregar menús predeterminados.</p>
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
                        <h5 class="card-title fw-bold">Menú Recomendado #{{ menu.id }}</h5>
                        <p class="card-text text-muted small">
                            {{ menu.items.length }} items | {{ menu.nutricion_total.calorias.toFixed(0) }} kcal | {{ formatCurrency(menu.nutricion_total.costo_total) }}
                        </p>
                        <ul class="list-unstyled mt-2 mb-3 small">
                           <li v-for="item in menu.items.slice(0, 3)" :key="item.alimento_id">
                                <i class="fas fa-check text-success me-1"></i> {{ item.nombre }} ({{ item.cantidad }}x)
                           </li>
                           <li v-if="menu.items.length > 3" class="text-muted">... y más</li>
                        </ul>
                        <div class="mt-auto">
                            <button class="btn btn-primary-nb w-100" @click="addMenuToProfile(menu)">
                                Agregar a Mis Loncheras
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
