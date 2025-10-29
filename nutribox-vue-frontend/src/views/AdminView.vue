<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { isAdmin } from '@/utils/user'; // Para verificar si realmente es Admin (doble chequeo)
import authService from '@/services/auth.service'; // Para logout si falla
import AppLayout from '@/components/AppLayout.vue'; // Asegura que se use el layout

const foods = ref([]);
const isLoading = ref(true);
const isUserAdmin = computed(() => isAdmin()); // Verifica el rol

// Función para formatear moneda (igual que en otras vistas)
function formatCurrency(value) {
    const numberValue = Number(value);
    if (isNaN(numberValue)) return '$ 0';
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(numberValue);
}

// Carga TODOS los alimentos (incluyendo inactivos)
async function loadFoods() {
    isLoading.value = true;
    if (!isUserAdmin.value) { // Seguridad extra
        isLoading.value = false;
        Swal.fire('Acceso Denegado', 'No tienes permisos de administrador.', 'error');
        authService.logout(); // Desloguear si intenta acceder sin ser admin
        return;
    }
    try {
        // Pide 'all' para incluir activos e inactivos
        foods.value = await apiService.get('/foods?only_active=all');
        isLoading.value = false;
    } catch (error) {
        isLoading.value = false;
        Swal.fire('Error', error.message || 'No se pudieron cargar los alimentos', 'error');
         if (error.message.includes("Token inválido") || error.message.includes("401")) {
             authService.logout();
        }
    }
}

// --- MODAL PARA AGREGAR ALIMENTO (Igual que en AlimentosView) ---
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
            await apiService.post('/foods', formValues); // Llama al endpoint protegido
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
            // Retorna solo los campos que pueden cambiar (PATCH)
            return { nombre, kcal, proteinas, carbos, costo };
        }
    });

    if (formValues) {
        try {
            Swal.fire({ title: 'Actualizando...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });
            // Usa concatenación simple para la URL del PATCH
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
            // Llama al endpoint PATCH solo con el nuevo estado 'activo'
            // Usa concatenación simple para la URL
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


onMounted(() => {
    loadFoods();
});
</script>

<template>
  <AppLayout>
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

        <div class="card p-4 card-shadow">
            <div v-if="isLoading" class="text-center p-5">
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
    </main>
  </AppLayout>
</template>

<style scoped>
/* Estilos específicos para esta vista si son necesarios */
.table td, .table th {
    vertical-align: middle;
}
</style>
