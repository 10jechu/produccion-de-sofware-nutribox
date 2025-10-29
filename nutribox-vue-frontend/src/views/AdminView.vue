<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { isAdmin, getUserDetail } from '@/utils/user'; // getUserDetail para obtener el ID del admin
import authService from '@/services/auth.service';

const foods = ref([]);
const adminLunchboxes = ref([]); // <-- NUEVO: Para guardar las loncheras del admin
const isLoadingFoods = ref(true);
const adminLunchboxesLoading = ref(true); // <-- NUEVO: Estado de carga para loncheras
const isUserAdmin = computed(() => isAdmin());
const adminUserId = computed(() => getUserDetail()?.id); // <-- NUEVO: Obtener el ID del admin

// Función para formatear fecha
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const parts = dateString.split('-');
    const date = new Date(Date.UTC(parts[0], parts[1] - 1, parts[2]));
    return date.toLocaleDateString('es-CO', { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' });
}

// Función para formatear moneda
function formatCurrency(value) {
    const numberValue = Number(value);
    if (isNaN(numberValue)) return '$ 0';
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(numberValue);
}

// Carga TODOS los alimentos (incluyendo inactivos)
async function loadFoods() {
    isLoadingFoods.value = true;
    if (!isUserAdmin.value) { /* ... (manejo de error como antes) ... */ return; }
    try {
        foods.value = await apiService.get('/foods?only_active=all');
        isLoadingFoods.value = false;
    } catch (error) {
        isLoadingFoods.value = false;
        Swal.fire('Error', error.message || 'No se pudieron cargar los alimentos', 'error');
         if (error.message.includes("Token inválido") || error.message.includes("401")) { authService.logout(); }
    }
}

// --- NUEVO: Cargar Loncheras creadas por el Admin ---
async function loadAdminLunchboxes() {
    adminLunchboxesLoading.value = true;
    if (!isUserAdmin.value || !adminUserId.value) {
      adminLunchboxesLoading.value = false;
      return;
    }
    try {
        // Asumiendo que las loncheras del admin se crean bajo su propio ID (necesitaría un hijo de prueba)
        // O podríamos necesitar un filtro específico si se asocian a un 'hijo fantasma'
        // Por ahora, listamos TODAS las loncheras y el admin elegirá. Ajustar si es necesario.
        const allLunchboxes = await apiService.get('/lunchboxes');
        // Filtramos aquí, pero idealmente el backend debería filtrar por `creator_id` si lo tuvieras
        adminLunchboxes.value = allLunchboxes; // Mostramos todas por simplicidad, ¡ajustar!
        adminLunchboxesLoading.value = false;
    } catch (error) {
        adminLunchboxesLoading.value = false;
        console.error("Error cargando loncheras del admin:", error);
        Swal.fire('Error', 'No se pudieron cargar las loncheras para marcar.', 'error');
    }
}

// --- MODAL PARA AGREGAR ALIMENTO (Sin cambios) ---
const showAddFoodModal = async () => { /* ... (código como antes) ... */ };

// --- MODAL PARA EDITAR ALIMENTO (Sin cambios) ---
const showEditFoodModal = async (foodToEdit) => { /* ... (código como antes) ... */ };

// --- FUNCIÓN PARA ACTIVAR/DESACTIVAR ALIMENTO (Sin cambios) ---
const toggleFoodStatus = async (food) => { /* ... (código como antes) ... */ };

// --- NUEVO: Función para Marcar Lonchera como Predeterminada ---
const markAsPredetermined = async (id) => {
    const result = await Swal.fire({
        title: "¿Marcar como Menú Predeterminado?",
        text: "Esta lonchera estará visible para todos los usuarios en la sección de Menús.",
        icon: 'question', // Cambiado a 'question'
        showCancelButton: true,
        confirmButtonColor: '#4CAF50',
        cancelButtonColor: '#6c757d', // Gris
        confirmButtonText: 'Sí, Marcar',
        cancelButtonText: 'Cancelar'
    });

    if (result.isConfirmed) {
        try {
            Swal.fire({ title: 'Marcando...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });
            await apiService.patch('/lunchboxes/' + id, { es_predeterminada: true });
            Swal.close();
            Swal.fire('¡Éxito!', 'Menú marcado y visible para todos.', 'success');
            await loadAdminLunchboxes(); // Recarga la lista de loncheras
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'No se pudo marcar la lonchera.', 'error');
        }
    }
};

onMounted(() => {
    loadFoods();
    loadAdminLunchboxes(); // <-- NUEVO: Carga las loncheras del admin al montar
});
</script>

<template>
  <main class="flex-grow-1 p-4 bg-light">
      <div class="d-flex justify-content-between align-items-center mb-4">
          <div>
              <h1 class="h3 text-danger">Panel de Administración - Alimentos</h1>
              <p class="text-muted">Gestionar el catálogo completo de alimentos (CRUD).</p>
          </div>
          <button class="btn btn-primary-nb" @click="showAddFoodModal">
              <i class="fas fa-plus me-1"></i> Agregar Alimento
          </button>
      </div>
      <div class="card p-4 card-shadow mb-5"> {/* Añadido mb-5 para separar secciones */}
          {/* ... (Tabla de alimentos como antes) ... */}
          <div v-if="isLoadingFoods" class="text-center p-5">...</div>
          <div v-else class="table-responsive">...</div>
      </div>


      <div class="card p-4 card-shadow">
          <div class="d-flex justify-content-between align-items-center mb-3">
              <div>
                  <h1 class="h3 text-danger">Panel de Administración - Menús Predeterminados</h1>
                  <p class="text-muted">Marcar loncheras creadas para que sean visibles a todos.</p>
              </div>
              <router-link to="/crear-lonchera" class="btn btn-outline-primary btn-sm">
                  <i class="fas fa-plus me-1"></i> Crear Lonchera Base
              </router-link>
          </div>
          <p class="text-muted small mb-3">Instrucción: Crea la lonchera en el panel principal (asígnale a un hijo de prueba si es necesario) y luego márcala aquí como predeterminada.</p>

          <div v-if="adminLunchboxesLoading" class="text-center p-5">
              <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
              <p class="mt-2 text-muted">Cargando loncheras...</p>
          </div>
          <div v-else-if="adminLunchboxes.length === 0" class="text-center p-5 text-muted">
              No hay loncheras creadas para marcar.
          </div>
          <div v-else class="table-responsive">
              <table class="table table-hover align-middle">
                  <thead>
                      <tr>
                          <th>ID</th>
                          <th>Fecha Creación/Ref</th>
                          <th>Estado Actual</th>
                          <th>Es Predeterminada</th>
                          <th>Acción</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="lb in adminLunchboxes" :key="lb.id">
                          <td>#{{ lb.id }}</td>
                          <td>{{ formatDate(lb.fecha) }}</td>
                          <td>
                              <span :class="['badge', lb.estado === 'Borrador' ? 'bg-warning text-dark' : 'bg-secondary']">
                                  {{ lb.estado }}
                              </span>
                          </td>
                          <td>
                              <span :class="['badge', lb.es_predeterminada ? 'bg-success' : 'bg-light text-dark']">
                                  {{ lb.es_predeterminada ? 'Sí' : 'No' }}
                              </span>
                          </td>
                          <td>
                              <button
                                  :disabled="lb.es_predeterminada"
                                  :class="['btn', 'btn-sm', lb.es_predeterminada ? 'btn-outline-secondary disabled' : 'btn-primary-nb']"
                                  @click="markAsPredetermined(lb.id)"
                                  :title="lb.es_predeterminada ? 'Ya está marcada' : 'Marcar como Menú Predeterminado'"
                              >
                                  <i :class="['fas', lb.es_predeterminada ? 'fa-check' : 'fa-star']"></i>
                                  {{ lb.es_predeterminada ? ' Marcada' : ' Marcar' }}
                              </button>
                          </td>
                      </tr>
                  </tbody>
              </table>
          </div>
      </div>
  </main>
</template>

<style scoped>
.table td, .table th { vertical-align: middle; }
</style>
