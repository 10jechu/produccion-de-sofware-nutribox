<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { getUserDetail, hasRequiredMembership, isAdmin } from '@/utils/user'; // Importar isAdmin
import authService from '@/services/auth.service';
import { useRouter } from 'vue-router';

const router = useRouter();
const menus = ref([]); 
const userData = ref(null);
const isLoading = ref(true);
const children = ref([]); 

// Verifica si el usuario es Admin
const isUserAdmin = computed(() => isAdmin()); 
// Verifica si el usuario tiene plan Estándar o superior para poder agregar menús
const canAddMenu = computed(() => hasRequiredMembership('Estandar'));

function formatCurrency(value) {
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(value || 0);
}

async function loadInitialData() {
    userData.value = getUserDetail();
    if (!userData.value) {
        authService.logout();
        return;
    }

    try {
        // Cargar hijos del usuario actual para la lista de destino (si no es admin)
        if (!isUserAdmin.value) {
             const childrenList = await apiService.get('/children?usuario_id=' + userData.value.id);
             children.value = childrenList;
        }
    } catch (error) {
        console.error("Error cargando hijos:", error);
    }
}

// Función para cargar los menús desde el backend
async function loadMenus() {
    isLoading.value = true;
    
    // Si no es Admin y no tiene plan Estándar, no cargamos nada más que la advertencia
    if (!canAddMenu.value && !isUserAdmin.value) {
        isLoading.value = false;
        return;
    }

    try {
         const baseMenus = await apiService.get('/menus');
        
        const detailedMenusPromises = baseMenus.map(menu => 
             apiService.get(`/lunchboxes/${menu.id}/detail`)
        );
        const detailedMenus = await Promise.all(detailedMenusPromises);

        menus.value = detailedMenus;
        isLoading.value = false;

    } catch (error) {
        isLoading.value = false;
        Swal.fire('Error', `No se pudieron cargar los menús predeterminados: ${error.message}`, 'error');
        menus.value = [];
    }
}

// Función para copiar un menú (para usuarios Estándar/Premium)
async function addMenuToProfile(menuId) {
    if (children.value.length === 0) {
         Swal.fire('Advertencia', 'Debes tener al menos un hijo registrado para poder agregar un menú a tu perfil.', 'warning');
         return;
    }
    
    const inputOptions = children.value.reduce((acc, child) => {
        acc[child.id] = child.nombre;
        return acc;
    }, {});

    const { value: targetHijoId } = await Swal.fire({
        title: 'Selecciona el Hijo',
        text: '¿A qué hijo deseas asignar este menú?',
        input: 'select',
        inputOptions: inputOptions,
        inputPlaceholder: 'Selecciona un hijo',
        showCancelButton: true,
        confirmButtonText: 'Copiar Menú'
    });

    if (targetHijoId) {
        try {
            Swal.showLoading();

            await apiService.post(`/lunchboxes/${menuId}/copy`, {
                target_hijo_id: parseInt(targetHijoId)
            });

            Swal.close();
            Swal.fire({
                icon: 'success',
                title: '¡Menú Agregado!',
                text: 'El menú se ha copiado como una nueva lonchera en estado "Borrador".',
                timer: 2500,
                showConfirmButton: false
            });

            setTimeout(() => {
                 router.push('/mis-loncheras');
            }, 1500);

        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'Error al copiar menú.', 'error');
        }
    }
}

// --- NUEVA FUNCIÓN: ELIMINAR MENÚ (ADMIN) ---
async function deleteMenu(menuId, menuName) {
    const result = await Swal.fire({
        title: `¿Eliminar Menú "${menuName}"?`,
        text: "Esta acción eliminará el menú base y es permanente.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#DC3545', 
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, Eliminar'
    });

    if (result.isConfirmed) {
        try {
            Swal.showLoading();
            // Los menús son loncheras base, así que usamos el endpoint DELETE /lunchboxes/{id}
            await apiService.delete(`/lunchboxes/${menuId}`);
            Swal.close();
            Swal.fire('Éxito', 'Menú base eliminado correctamente.', 'success');
            await loadMenus(); // Recargar la lista
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'Error al eliminar el menú base.', 'error');
        }
    }
}

// --- NUEVA FUNCIÓN: CREAR MENÚ (ADMIN) ---
function createMenu() {
    // Redirigir a Crear Lonchera, ya que el Admin crea el menú igual que una lonchera normal
    router.push('/crear-lonchera'); 
}


onMounted(() => {
    loadInitialData();
    loadMenus();
});

</script>

<template>
    <main class="flex-grow-1 p-4 bg-light">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3">Menús Predeterminados</h1>
                <p class="text-muted">Explora nuestras loncheras recomendadas y agrégalas a tu plan.</p>
            </div>
            <button v-if="isUserAdmin" class="btn btn-danger" @click="createMenu">
                <i class="fas fa-plus me-1"></i> Crear Menú Base
            </button>
        </div>

        <div v-if="!canAddMenu && !isUserAdmin && !isLoading" class="card p-5 text-center card-shadow border-warning">
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
                        <div class="d-flex justify-content-between align-items-center mb-3">
                             <h5 class="card-title fw-bold mb-0">{{ menu.estado }}</h5>
                             <button v-if="isUserAdmin" class="btn btn-sm btn-outline-danger" title="Eliminar Menú Base" @click="deleteMenu(menu.id, menu.estado)">
                                <i class="fas fa-trash-alt"></i>
                             </button>
                        </div>
                        
                        <p class="card-text text-muted small mb-3">
                            Una selección balanceada con aprox. {{ menu.nutricion_total?.calorias?.toFixed(0) ?? 'N/A' }} kcal.
                        </p>
                        
                        <h6 class="fw-bold small">Alimentos ({{ menu.items?.length ?? 0 }}):</h6>
                        <ul class="list-unstyled mt-0 mb-4 small flex-grow-1">
                           <li v-for="item in menu.items" :key="item.alimento_id" class="mb-1 d-flex justify-content-between">
                                <span>{{ item.nombre }} (x{{ item.cantidad }})</span>
                                <span class="fw-bold">{{ item.kcal.toFixed(0) }} kcal</span>
                           </li>
                           </ul>

                        <div class="border-top pt-3">
                            <div class="d-flex justify-content-between small fw-bold mb-2">
                                <span>Total Calorías:</span>
                                <span>{{ menu.nutricion_total?.calorias?.toFixed(0) ?? 'N/A' }} kcal</span>
                            </div>
                            <div class="d-flex justify-content-between small fw-bold mb-3">
                                <span>Costo Total:</span>
                                <span class="text-danger">{{ formatCurrency(menu.nutricion_total?.costo_total) }}</span>
                            </div>
                        </div>

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
    border-left: 5px solid var(--nb-secondary, #66BB6A);
}

.menu-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--nb-shadow-medium);
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
