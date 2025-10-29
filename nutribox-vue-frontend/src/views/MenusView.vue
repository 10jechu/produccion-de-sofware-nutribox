<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { getUserDetail, hasRequiredMembership } from '@/utils/user';
import authService from '@/services/auth.service';
import { useRouter } from 'vue-router';

const router = useRouter();
const menus = ref([]); // Almacenará los detalles de las loncheras/menús
const userData = ref(null);
const isLoading = ref(true);

// Verifica si el usuario tiene plan Estándar o superior para poder agregar menús
const canAddMenu = computed(() => hasRequiredMembership('Estandar'));

// Función para cargar los menús desde el backend
async function loadMenus() {
    isLoading.value = true;
    userData.value = getUserDetail(); // Obtiene datos del usuario logueado
    if (!userData.value) {
        authService.logout(); // Si no hay usuario, redirige a login
        return;
    }

    // No carga menús si el plan es Básico
    if (!canAddMenu.value) {
        isLoading.value = false;
        return;
    }

    try {
        // --- Lógica para obtener Menús ---
        // Opción A: Filtrar loncheras existentes (ej. por usuario_id del Admin, asumiendo ID=1)
        // const allLunchboxes = await apiService.get('/lunchboxes');
        // const potentialMenus = allLunchboxes.filter(lb => lb.usuario_id === 1 && lb.id !== userData.value.id); // Ejemplo: loncheras del admin

        // Opción B (Recomendada): Usar un endpoint específico si lo creas en el backend
         const potentialMenus = await apiService.get('/menus'); // Asumiendo que creas GET /api/v1/menus/

        // Necesitamos el detalle para mostrar algo útil (ej. Nro. Items)
        const detailedMenusPromises = potentialMenus.slice(0, 6).map(menu => // Limita a 6 menús
             apiService.get(`/lunchboxes/${menu.id}/detail`) // Obtiene detalle completo
        );
        const detailedMenus = await Promise.all(detailedMenusPromises);

        menus.value = detailedMenus; // Guarda los menús detallados
        isLoading.value = false;

    } catch (error) {
        isLoading.value = false;
        // Muestra un error más específico si falla la carga
        Swal.fire('Error', `No se pudieron cargar los menús predeterminados: ${error.message}`, 'error');
        menus.value = []; // Asegura que la lista esté vacía en caso de error
    }
}

// Función para copiar un menú a las loncheras del usuario
async function addMenuToProfile(menuId) {
    // Verifica si el usuario tiene hijos (necesario para asignar la copia)
    const userDetail = getUserDetail(); // Recarga por si acaso
    // Busca el primer hijo del usuario (o podrías permitir seleccionar a cuál hijo copiarlo)
    const childrenResponse = await apiService.get(`/children?usuario_id=${userDetail.id}`);
    const firstHijo = childrenResponse.length > 0 ? childrenResponse[0] : null;

    if (!firstHijo) {
         Swal.fire('Advertencia', 'Debes tener al menos un hijo registrado para poder agregar un menú a tu perfil.', 'warning');
         return;
    }

    try {
        Swal.fire({ title: 'Copiando Menú...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });

        // --- Lógica Backend para Copiar (DEBE EXISTIR EN TU API) ---
        // Idealmente, tendrías un endpoint como: POST /api/v1/menus/{menuId}/copy-to-user/{userId}/child/{hijoId}
        // O una versión más simple: POST /api/v1/lunchboxes/{menuId}/copy-as-draft?hijo_id={firstHijo.id}

        // --- Simulación si no tienes el endpoint de copia aún ---
        // 1. Obtener detalle del menú original
        const originalMenu = await apiService.get(`/lunchboxes/${menuId}/detail`);
        // 2. Crear una nueva lonchera (borrador) para el primer hijo
        const newLunchbox = await apiService.post('/lunchboxes', {
            hijo_id: firstHijo.id,
            fecha: new Date().toISOString().split("T")[0], // Fecha de hoy
            estado: "Borrador",
            direccion_id: null // Sin dirección por defecto
        });
        // 3. Añadir cada item del menú original a la nueva lonchera
        for (const item of originalMenu.items) {
            await apiService.post(`/lunchboxes/${newLunchbox.id}/items`, {
                alimento_id: item.alimento_id,
                cantidad: item.cantidad
            });
        }
        // --- Fin Simulación ---

        Swal.close();
        Swal.fire({
            icon: 'success',
            title: '¡Menú Agregado!',
            text: 'El menú se ha copiado como una nueva lonchera en estado "Borrador" a "Mis Loncheras".',
            timer: 2500, // Cierra automáticamente
            showConfirmButton: false
        });

        // Redirige a "Mis Loncheras" después de un momento
        setTimeout(() => {
             router.push('/mis-loncheras');
        }, 1500);

    } catch (error) {
        Swal.close();
        Swal.fire('Error', `No se pudo agregar el menú a tu perfil: ${error.message}`, 'error');
    }
}

// Carga los menús cuando el componente se monta
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

        <div v-if="!canAddMenu && !isLoading" class="card p-5 text-center card-shadow border-warning">
            <i class="fas fa-lock text-warning mb-3" style="font-size: 48px;"></i>
            <h3 class="h4">Función de Plan Estándar o Premium</h3>
            <p class="text-muted mb-4">Para explorar y agregar menús predeterminados a tu perfil, necesitas actualizar tu plan.</p>
            <router-link to="/perfil" class="btn btn-warning w-auto mx-auto text-dark fw-bold">Ver Planes</router-link>
        </div>

        <div v-else-if="isLoading" class="text-center p-5">
            <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
            <p class="mt-2 text-muted">Cargando menús disponibles...</p>
        </div>

        <div v-else-if="menus.length === 0" class="row g-4">
            <div class="col-12">
                <div class="card p-5 text-center card-shadow">
                     <i class="fas fa-folder-open text-muted mb-3" style="font-size: 48px;"></i>
                     <h4 class="h5">No hay menús predeterminados disponibles</h4>
                     <p class="text-muted">Pronto agregaremos nuevas opciones recomendadas.</p>
                </div>
            </div>
        </div>

        <div v-else id="menusContainer" class="row g-4">
            <div v-for="menu in menus" :key="menu.id" class="col-lg-4 col-md-6">
                <div class="card h-100 card-shadow menu-card">
                    <div class="card-body d-flex flex-column">
                        <div class="d-flex align-items-center mb-3">
                             <i class="fas fa-utensils fs-4 text-primary-nb me-3"></i>
                             <h5 class="card-title fw-bold mb-0">Menú Recomendado #{{ menu.id }}</h5>
                        </div>
                        <p class="card-text text-muted small mb-3">
                            Una selección balanceada con aprox.
                            <span class="fw-bold">{{ menu.nutricion_total?.calorias?.toFixed(0) ?? 'N/A' }} kcal</span>.
                        </p>
                        <ul class="list-unstyled mt-2 mb-4 small flex-grow-1">
                           <li class="mb-1"><i class="fas fa-check text-success me-2"></i> {{ menu.items?.length ?? 0 }} ítems variados</li>
                           <li class="mb-1"><i class="fas fa-star text-warning me-2"></i> Popular entre niños</li>
                           <li class="mb-1"><i class="fas fa-leaf text-secondary me-2"></i> Incluye frutas/verduras</li>
                           </ul>
                        <div class="mt-auto">
                            <button class="btn btn-primary-nb w-100 btn-add-menu" @click="addMenuToProfile(menu.id)">
                                <i class="fas fa-plus-circle me-2"></i> Agregar a Mis Loncheras
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped>
.menu-card {
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    border-left: 5px solid var(--nb-secondary, #66BB6A); /* Acento verde secundario */
}

.menu-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--nb-shadow-medium); /* Sombra más pronunciada al pasar */
}

.card-title {
    color: var(--nb-text-dark);
}

.btn-add-menu {
    font-weight: 600;
}

.card-shadow.border-warning {
    border: 1px solid var(--nb-warning, #FF9800);
}
</style>