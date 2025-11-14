<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { getUserDetail, hasRequiredMembership, isAdmin } from '@/utils/user';
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

// Función para cargar los menús desde el backend - CORREGIDO: usuarios Free pueden ver
async function loadMenus() {
    isLoading.value = true;

    try {
        const baseMenus = await apiService.get('/menus');

        // Cargar detalles de cada menú
        const detailedMenusPromises = baseMenus.map(menu =>
            apiService.get(`/lunchboxes/${menu.id}/detail`)
        );
        const detailedMenus = await Promise.all(detailedMenusPromises);

        menus.value = detailedMenus;
        isLoading.value = false;

    } catch (error) {
        isLoading.value = false;
        console.error("Error cargando menús:", error);
        // No mostrar error para usuarios Free
        menus.value = [];
    }
}

// Función para copiar un menú (para usuarios Estándar/Premium) - CORREGIDO
async function addMenuToProfile(menuId) {
    if (!canAddMenu.value) {
        Swal.fire({
            icon: 'info',
            title: 'Actualiza tu Plan',
            html: `
                <p>Para <strong>agregar menús a tu perfil</strong> necesitas actualizar a plan <strong>Estándar o Premium</strong>.</p>
                <p class="text-muted mb-3">Actualmente puedes visualizar los menús pero no copiarlos.</p>
            `,
            confirmButtonText: 'Ver Planes',
            showCancelButton: true,
            cancelButtonText: 'Seguir Viendo'
        }).then((result) => {
            if (result.isConfirmed) {
                router.push('/app/perfil');
            }
        });
        return;
    }

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
        confirmButtonText: 'Copiar Menú',
        cancelButtonText: 'Cancelar'
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
                router.push('/app/mis-loncheras');
            }, 1500);

        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'Error al copiar menú.', 'error');
        }
    }
}

// --- FUNCIÓN: ELIMINAR MENÚ (ADMIN) ---
async function deleteMenu(menuId, menuName) {
    const result = await Swal.fire({
        title: `¿Eliminar Menú "${menuName}"?`,
        text: "Esta acción eliminará el menú base y es permanente.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#DC3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, Eliminar',
        cancelButtonText: 'Cancelar'
    });

    if (result.isConfirmed) {
        try {
            Swal.showLoading();
            await apiService.delete(`/lunchboxes/${menuId}`);
            Swal.close();
            Swal.fire('Éxito', 'Menú base eliminado correctamente.', 'success');
            await loadMenus();
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'Error al eliminar el menú base.', 'error');
        }
    }
}

// --- FUNCIÓN: CREAR MENÚ (ADMIN) ---
function createMenu() {
  // ✅ CORREGIDO: Por ahora el admin crea menús como loncheras normales
  // hasta que tengamos endpoint específico para menús
  router.push('/app/crear-lonchera');
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
                <p class="text-muted">Explora nuestras loncheras recomendadas.</p>
            </div>
            <button v-if="isUserAdmin" class="btn btn-success" @click="createMenu">
                <i class="fas fa-plus me-1"></i> Crear Menú Base
            </button>
        </div>

        <!-- Mensaje para usuarios Free -->
        <div v-if="!canAddMenu && !isUserAdmin && !isLoading" class="alert alert-info mb-4">
            <div class="d-flex align-items-center">
                <i class="fas fa-info-circle me-3 fs-4"></i>
                <div class="flex-grow-1">
                    <h6 class="alert-heading mb-1">Plan Free - Solo Visualización</h6>
                    <p class="mb-0">Puedes ver los menús predeterminados. Para <strong>agregarlos a tu perfil y personalizarlos</strong>, actualiza a plan <strong>Estándar o Premium</strong>.</p>
                </div>
                <router-link to="/app/perfil" class="btn btn-warning ms-3 text-dark fw-bold">
                    Ver Planes
                </router-link>
            </div>
        </div>

        <div v-if="isLoading" class="text-center p-5">
            <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
            <p class="mt-2 text-muted">Cargando menús disponibles...</p>
        </div>

        <div v-else-if="menus.length === 0" class="row g-4">
            <div class="col-12">
                <div class="card p-5 text-center card-shadow">
                     <i class="fas fa-folder-open text-muted mb-3" style="font-size: 48px;"></i>
                     <h4 class="h5">No hay menús predeterminados disponibles</h4>
                     <p class="text-muted">El administrador aún no ha creado menús base.</p>
                     <button v-if="isUserAdmin" class="btn btn-success mt-3" @click="createMenu">
                         <i class="fas fa-plus me-1"></i> Crear Primer Menú
                     </button>
                </div>
            </div>
        </div>

        <div v-else id="menusContainer" class="row g-4">
            <div v-for="menu in menus" :key="menu.id" class="col-lg-4 col-md-6">
                <div class="card h-100 card-shadow menu-card">
                    <div class="card-body d-flex flex-column">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                             <h5 class="card-title fw-bold mb-0">{{ menu.hijo?.nombre || 'Menú Base' }}</h5>
                             <button v-if="isUserAdmin" class="btn btn-sm btn-outline-danger" title="Eliminar Menú Base" @click="deleteMenu(menu.id, menu.hijo?.nombre)">
                                <i class="fas fa-trash-alt"></i>
                             </button>
                        </div>

                        <p class="card-text text-muted small mb-3">
                            Una selección balanceada con aprox. {{ menu.nutricion_total?.calorias?.toFixed(0) || 'N/A' }} kcal.
                        </p>

                        <h6 class="fw-bold small">Alimentos ({{ menu.items?.length || 0 }}):</h6>
                        <ul class="list-unstyled mt-0 mb-4 small flex-grow-1">
                           <li v-for="item in menu.items" :key="item.alimento_id" class="mb-1 d-flex justify-content-between">
                                <span>{{ item.nombre }} (x{{ item.cantidad }})</span>
                                <span class="fw-bold">{{ item.kcal?.toFixed(0) || 0 }} kcal</span>
                           </li>
                        </ul>

                        <div class="border-top pt-3">
                            <div class="d-flex justify-content-between small fw-bold mb-2">
                                <span>Total Calorías:</span>
                                <span>{{ menu.nutricion_total?.calorias?.toFixed(0) || 'N/A' }} kcal</span>
                            </div>
                            <div class="d-flex justify-content-between small fw-bold mb-3">
                                <span>Costo Total:</span>
                                <span class="text-danger">{{ formatCurrency(menu.nutricion_total?.costo_total) }}</span>
                            </div>
                        </div>

                        <div class="mt-auto">
                            <button 
                                class="btn w-100" 
                                :class="canAddMenu ? 'btn-primary-nb' : 'btn-outline-secondary'" 
                                @click="addMenuToProfile(menu.id)"
                                :disabled="!canAddMenu && !isUserAdmin"
                            >
                                <i class="fas fa-plus-circle me-2"></i> 
                                {{ canAddMenu ? 'Agregar a Mis Loncheras' : 'Actualizar Plan para Agregar' }}
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