<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { isAdmin, getUserDetail } from '@/utils/user';
import authService from '@/services/auth.service';

const foods = ref([]);
const adminLunchboxes = ref([]);
const isLoadingFoods = ref(true);
const adminLunchboxesLoading = ref(true);
const isUserAdmin = computed(() => isAdmin());
const adminUserId = computed(() => getUserDetail()?.id);

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
    if (!isUserAdmin.value) {
        isLoadingFoods.value = false;
        Swal.fire('Acceso Denegado', 'No tienes permisos de administrador.', 'error');
        authService.logout();
        return;
    }
    try {
        foods.value = await apiService.get('/foods?only_active=all');
        isLoadingFoods.value = false;
    } catch (error) {
        isLoadingFoods.value = false;
        Swal.fire('Error', error.message || 'No se pudieron cargar los alimentos', 'error');
         if (error.message.includes("Token inválido") || error.message.includes("401")) { authService.logout(); }
    }
}

// Cargar Loncheras creadas por el Admin
async function loadAdminLunchboxes() {
    adminLunchboxesLoading.value = true;
    if (!isUserAdmin.value || !adminUserId.value) {
      adminLunchboxesLoading.value = false;
      return;
    }
    try {
        const allLunchboxes = await apiService.get('/lunchboxes');
        // TODO: Idealmente, filtrar en backend por loncheras creadas por el admin
        adminLunchboxes.value = allLunchboxes;
        adminLunchboxesLoading.value = false;
    } catch (error) {
        adminLunchboxesLoading.value = false;
        console.error("Error cargando loncheras del admin:", error);
        Swal.fire('Error', 'No se pudieron cargar las loncheras para marcar.', 'error');
    }
}

// --- MODAL PARA AGREGAR ALIMENTO ---
const showAddFoodModal = async () => {
    const { value: formValues } = await Swal.fire({
        title: "Agregar Nuevo Alimento",
        html: `
            <input id="swal-nombre" class="swal2-input form-control" placeholder="Nombre del alimento" required>
            <input id="swal-kcal" type="number" step="0.1" class="swal2-input form-control" placeholder="Calorías (kcal)" required>
            <input id="swal-proteinas" type="number" step="0.1" class="swal2-input form-control" placeholder="Proteínas (g)" required>
            <input id="swal-carbos" type="number" step="0.1" class="swal2-input form-control" placeholder="Carbohidratos (g)" required>
            <input id="swal-costo" type="number" step="1" class="swal2-input form-control" placeholder="Costo Unitario (COP)" value="0" required>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: "#4CAF50",
        cancelButtonColor: "#DC3545",
        confirmButtonText: "Guardar Alimento",
        cancelButtonText: "Cancelar",
        preConfirm: () => {
            const nombre = document.getElementById("swal-nombre").value;
            const kcal = parseFloat(document.getElementById("swal-kcal").value);
            const proteinas = parseFloat(document.getElementById("swal-proteinas").value);
            const carbos = parseFloat(document.getElementById("swal-carbos").value);
            const costo = parseFloat(document.getElementById("swal-costo").value);

            if (!nombre || isNaN(kcal) || isNaN(proteinas) || isNaN(carbos) || isNaN(costo)) {
                Swal.showValidationMessage("Todos los campos son requeridos y deben ser números válidos."); return false;
            }
            if (kcal < 0 || proteinas < 0 || carbos < 0 || costo < 0) {
                 Swal.showValidationMessage("Los valores numéricos no pueden ser negativos."); return false;
            }
            return { nombre, kcal, proteinas, carbos, costo, activo: true };
        }
    });

    if (formValues) {
        try {
            Swal.fire({ title: 'Guardando...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });
            await apiService.post('/foods', formValues);
            Swal.close();
            Swal.fire('¡Éxito!', 'Alimento agregado correctamente', 'success');
            await loadFoods();
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'No se pudo agregar el alimento', 'error');
        }
    }
};

// --- MODAL PARA EDITAR ALIMENTO ---
const showEditFoodModal = async (foodToEdit) => {
    if (!foodToEdit) return;

    const { value: formValues } = await Swal.fire({
        title: "Editar Alimento",
        html: `
            <input id="swal-nombre" class="swal2-input form-control" placeholder="Nombre" value="${foodToEdit.nombre}" required>
            <input id="swal-kcal" type="number" step="0.1" class="swal2-input form-control" placeholder="Calorías (kcal)" value="${foodToEdit.kcal}" required>
            <input id="swal-proteinas" type="number" step="0.1" class="swal2-input form-control" placeholder="Proteínas (g)" value="${foodToEdit.proteinas}" required>
            <input id="swal-carbos" type="number" step="0.1" class="swal2-input form-control" placeholder="Carbohidratos (g)" value="${foodToEdit.carbos}" required>
            <input id="swal-costo" type="number" step="1" class="swal2-input form-control" placeholder="Costo Unitario (COP)" value="${foodToEdit.costo}" required>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: "#4CAF50",
        cancelButtonColor: "#DC3545",
        confirmButtonText: "Guardar Cambios",
        preConfirm: () => {
            const nombre = document.getElementById("swal-nombre").value;
            const kcal = parseFloat(document.getElementById("swal-kcal").value);
            const proteinas = parseFloat(document.getElementById("swal-proteinas").value);
            const carbos = parseFloat(document.getElementById("swal-carbos").value);
            const costo = parseFloat(document.getElementById("swal-costo").value);

             if (!nombre || isNaN(kcal) || isNaN(proteinas) || isNaN(carbos) || isNaN(costo)) {
                Swal.showValidationMessage("Todos los campos son requeridos y deben ser números válidos."); return false;
            }
             if (kcal < 0 || proteinas < 0 || carbos < 0 || costo < 0) {
                 Swal.showValidationMessage("Los valores numéricos no pueden ser negativos."); return false;
            }
            return { nombre, kcal, proteinas, carbos, costo };
        }
    });

    if (formValues) {
        try {
            Swal.fire({ title: 'Actualizando...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });
            await apiService.patch('/foods/' + foodToEdit.id, formValues);
            Swal.close();
            Swal.fire('¡Éxito!', 'Alimento actualizado correctamente', 'success');
            await loadFoods();
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'No se pudo actualizar el alimento', 'error');
        }
    }
};

// --- FUNCIÓN PARA ACTIVAR/DESACTIVAR ALIMENTO ---
const toggleFoodStatus = async (food) => {
    if (!food) return;

    const actionText = food.activo ? "Desactivar" : "Activar";
    const confirmText = food.activo
        ? "Esto marcará el alimento como inactivo y no aparecerá en el catálogo para usuarios."
        : "Esto volverá a mostrar el alimento en el catálogo.";

    const result = await Swal.fire({
        title: `¿${actionText} alimento?`,
        text: confirmText,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#4CAF50',
        cancelButtonColor: '#DC3545',
        confirmButtonText: `Sí, ${actionText}`,
        cancelButtonText: 'Cancelar'
    });

    if (result.isConfirmed) {
        try {
            Swal.fire({ title: 'Cambiando estado...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });
            await apiService.patch('/foods/' + food.id, { activo: !food.activo });
            Swal.close();
            Swal.fire('¡Éxito!', `Alimento ${actionText.toLowerCase()}do correctamente`, 'success');
            await loadFoods();
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'No se pudo cambiar el estado del alimento', 'error');
        }
    }
};

// --- Función para Marcar Lonchera como Predeterminada ---
const markAsPredetermined = async (id) => {
    const result = await Swal.fire({
        title: "¿Marcar como Menú Predeterminado?",
        text: "Esta lonchera estará visible para todos los usuarios en la sección de Menús.",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#4CAF50',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, Marcar',
        cancelButtonText: 'Cancelar'
    });

    if (result.isConfirmed) {
        try {
            Swal.fire({ title: 'Marcando...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });
            await apiService.patch('/lunchboxes/' + id, { es_predeterminada: true });
            Swal.close();
            Swal.fire('¡Éxito!', 'Menú marcado y visible para todos.', 'success');
            await loadAdminLunchboxes();
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'No se pudo marcar la lonchera.', 'error');
        }
    }
};

onMounted(() => {
    loadFoods();
    loadAdminLunchboxes();
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

      <div class="card p-4 card-shadow mb-5"> <div v-if="isLoadingFoods" class="text-center p-5">
              <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
              <p class="mt-2 text-muted">Cargando alimentos...</p>
          </div>
          <div v-else class="table-responsive">
              <table class="table table-hover align-middle">
                  <thead>
                      <tr>
                          <th>Nombre</th>
                          <th>Kcal</th>
                          <th>Prot. (g)</th>
                          <th>Carb. (g)</th>
                          <th>Costo</th>
                          <th>Estado</th>
                          <th>Acciones</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="food in foods" :key="food.id">
                          <td>{{ food.nombre }}</td>
                          <td>{{ food.kcal?.toFixed(1) }}</td>
                          <td>{{ food.proteinas?.toFixed(1) }}</td>
                          <td>{{ food.carbos?.toFixed(1) }}</td>
                          <td>{{ formatCurrency(food.costo) }}</td>
                          <td>
                              <span :class="['badge', food.activo ? 'bg-success' : 'bg-danger']">
                                  {{ food.activo ? 'Activo' : 'Inactivo' }}
                              </span>
                          </td>
                          <td>
                              <button class="btn btn-sm btn-outline-warning me-1" @click="showEditFoodModal(food)" title="Editar Alimento">
                                  <i class="fas fa-edit"></i>
                              </button>
                              <button
                                :class="['btn', 'btn-sm', food.activo ? 'btn-outline-danger' : 'btn-outline-success']"
                                @click="toggleFoodStatus(food)"
                                :title="food.activo ? 'Desactivar Alimento' : 'Activar Alimento'">
                                  <i :class="['fas', food.activo ? 'fa-toggle-off' : 'fa-toggle-on']"></i>
                              </button>
                          </td>
                      </tr>
                      <tr v-if="foods.length === 0">
                           <td colspan="7" class="text-center text-muted py-4">
                              No hay alimentos registrados. ¡Agrega el primero!
                           </td>
                      </tr>
                  </tbody>
              </table>
          </div>
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
