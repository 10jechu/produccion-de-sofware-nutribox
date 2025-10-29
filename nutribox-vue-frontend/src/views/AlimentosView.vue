<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { isAdmin } from '@/utils/user'; // Para verificar si es admin

const foods = ref([]);
const isLoading = ref(true);

const isUserAdmin = computed(() => isAdmin()); // Verifica si el usuario logueado es Admin

// Formato de moneda COP
function formatCurrency(value) {
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(value || 0);
}

// Carga los alimentos desde la API
async function loadFoods() {
    isLoading.value = true;
    try {
        // Si es admin, carga 'all' (activos e inactivos), si no, solo 'true' (activos)
        const filter = isUserAdmin.value ? 'all' : 'true';
        foods.value = await apiService.get(`/foods?only_active=${filter}`);
        isLoading.value = false;
    } catch (error) {
        isLoading.value = false;
        Swal.fire('Error', error.message || 'No se pudieron cargar los alimentos', 'error');
    }
}

// --- FUNCIONES CRUD (Adaptadas de tu frontend antiguo) ---

// Mostrar modal para AGREGAR alimento
async function showAddFoodModal() {
    const { value: formValues } = await Swal.fire({
        title: "Agregar Nuevo Alimento",
        html: `
            <input id="swal-nombre" class="swal2-input form-control" placeholder="Nombre del alimento" required>
            <input id="swal-kcal" type="number" step="0.1" class="swal2-input form-control" placeholder="Calorías (kcal)" required>
            <input id="swal-proteinas" type="number" step="0.1" class="swal2-input form-control" placeholder="Proteínas (g)" required>
            <input id="swal-carbos" type="number" step="0.1" class="swal2-input form-control" placeholder="Carbohidratos (g)" required>
            <input id="swal-costo" type="number" step="0.01" class="swal2-input form-control" placeholder="Costo Unitario (COP)" value="0.00" required>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: "#4CAF50", // Verde
        cancelButtonColor: "#DC3545", // Rojo
        confirmButtonText: "Guardar Alimento",
        cancelButtonText: "Cancelar",
        preConfirm: () => {
            const nombre = document.getElementById("swal-nombre")?.value;
            const kcalStr = document.getElementById("swal-kcal")?.value;
            const proteinasStr = document.getElementById("swal-proteinas")?.value;
            const carbosStr = document.getElementById("swal-carbos")?.value;
            const costoStr = document.getElementById("swal-costo")?.value;

            // Validación robusta
            if (!nombre || !kcalStr || !proteinasStr || !carbosStr || !costoStr) {
                Swal.showValidationMessage("Todos los campos son requeridos.");
                return false;
            }
            const kcal = parseFloat(kcalStr);
            const proteinas = parseFloat(proteinasStr);
            const carbos = parseFloat(carbosStr);
            const costo = parseFloat(costoStr);

            if (isNaN(kcal) || isNaN(proteinas) || isNaN(carbos) || isNaN(costo)) {
                Swal.showValidationMessage("Los valores numéricos deben ser números válidos.");
                return false;
            }
            if (kcal < 0 || proteinas < 0 || carbos < 0 || costo < 0) {
                 Swal.showValidationMessage("Los valores numéricos no pueden ser negativos.");
                return false;
            }
            return { nombre, kcal, proteinas, carbos, costo };
        }
    });

    if (formValues) {
        try {
            Swal.showLoading();
            await apiService.post('/foods', formValues); // Llama a la API para crear
            Swal.close();
            Swal.fire('Éxito', 'Alimento agregado correctamente', 'success');
            await loadFoods(); // Recargar la lista de alimentos
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'No se pudo agregar el alimento', 'error');
        }
    }
}

// Mostrar modal para EDITAR alimento
async function showEditFoodModal(foodId) {
    const foodToEdit = foods.value.find(f => f.id === foodId);
    if (!foodToEdit) {
        Swal.fire("Error", "No se encontró el alimento para editar.", "error");
        return;
    }

    const { value: formValues } = await Swal.fire({
        title: "Editar Alimento",
        html: `
            <input id="swal-nombre" class="swal2-input form-control" placeholder="Nombre" value="${foodToEdit.nombre}" required>
            <input id="swal-kcal" type="number" step="0.1" class="swal2-input form-control" placeholder="Calorías (kcal)" value="${foodToEdit.kcal}" required>
            <input id="swal-proteinas" type="number" step="0.1" class="swal2-input form-control" placeholder="Proteínas (g)" value="${foodToEdit.proteinas}" required>
            <input id="swal-carbos" type="number" step="0.1" class="swal2-input form-control" placeholder="Carbohidratos (g)" value="${foodToEdit.carbos}" required>
            <input id="swal-costo" type="number" step="0.01" class="swal2-input form-control" placeholder="Costo Unitario (COP)" value="${foodToEdit.costo?.toFixed(2) ?? '0.00'}" required>
            <div class="form-check mt-3 text-start">
              <input class="form-check-input" type="checkbox" id="swal-activo" ${foodToEdit.activo ? 'checked' : ''}>
              <label class="form-check-label" for="swal-activo">
                Activo (disponible para seleccionar)
              </label>
            </div>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: "#4CAF50", // Verde
        cancelButtonColor: "#DC3545", // Rojo
        confirmButtonText: "Guardar Cambios",
        cancelButtonText: "Cancelar",
        preConfirm: () => {
            const nombre = document.getElementById("swal-nombre")?.value;
            const kcalStr = document.getElementById("swal-kcal")?.value;
            const proteinasStr = document.getElementById("swal-proteinas")?.value;
            const carbosStr = document.getElementById("swal-carbos")?.value;
            const costoStr = document.getElementById("swal-costo")?.value;
            const activo = document.getElementById("swal-activo")?.checked;

            // Validación (similar a agregar)
             if (!nombre || !kcalStr || !proteinasStr || !carbosStr || !costoStr) {
                Swal.showValidationMessage("Todos los campos son requeridos.");
                return false;
            }
            const kcal = parseFloat(kcalStr);
            const proteinas = parseFloat(proteinasStr);
            const carbos = parseFloat(carbosStr);
            const costo = parseFloat(costoStr);

             if (isNaN(kcal) || isNaN(proteinas) || isNaN(carbos) || isNaN(costo)) {
                Swal.showValidationMessage("Los valores numéricos deben ser números válidos.");
                return false;
            }
             if (kcal < 0 || proteinas < 0 || carbos < 0 || costo < 0) {
                 Swal.showValidationMessage("Los valores numéricos no pueden ser negativos.");
                return false;
            }
            // Devolvemos solo los campos que podrían cambiar (PATCH)
            return { nombre, kcal, proteinas, carbos, costo, activo }; // Incluye el estado 'activo'
        }
    });

    if (formValues) {
        try {
            Swal.showLoading();
            await apiService.patch(`/foods/${foodId}`, formValues); // Llama a la API con PATCH
            Swal.close();
            Swal.fire("Éxito", "Alimento actualizado correctamente", "success");
            await loadFoods(); // Recargar la lista
        } catch (error) {
            Swal.close();
            Swal.fire("Error", error.message || 'No se pudo actualizar el alimento', "error");
        }
    }
}

// Función para DESACTIVAR (soft delete) alimento
async function deleteFood(foodId) {
    const foodToDelete = foods.value.find(f => f.id === foodId);
     if (!foodToDelete) return;

    // Diferente mensaje si ya está inactivo (para reactivar)
    const isActive = foodToDelete.activo;
    const confirmTitle = isActive ? "¿Desactivar Alimento?" : "¿Reactivar Alimento?";
    const confirmText = isActive
        ? "Esta acción marcará el alimento como inactivo y no se podrá seleccionar en nuevas loncheras."
        : "Esta acción volverá a poner el alimento como activo y disponible.";
    const confirmButton = isActive ? 'Sí, desactivar' : 'Sí, reactivar';
    const successMessage = isActive ? 'Alimento desactivado' : 'Alimento reactivado';

    const result = await Swal.fire({
        title: confirmTitle,
        text: confirmText,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: isActive ? '#DC3545' : '#4CAF50', // Rojo para desactivar, Verde para activar
        cancelButtonColor: '#6c757d', // Gris
        confirmButtonText: confirmButton,
        cancelButtonText: 'Cancelar'
    });

    if (result.isConfirmed) {
        try {
            Swal.showLoading();
            // Si está activo, hacemos DELETE (soft delete en backend)
            // Si está inactivo, hacemos PATCH para poner activo: true
            if (isActive) {
                 await apiService.delete(`/foods/${foodId}`); // El backend hace soft delete
            } else {
                 await apiService.patch(`/foods/${foodId}`, { activo: true }); // Reactivamos
            }
            Swal.close();
            Swal.fire("Éxito", `${successMessage} correctamente`, "success");
            await loadFoods(); // Recargar la lista para que refleje el cambio de estado
        } catch (error) {
            Swal.close();
            Swal.fire("Error", error.message || `No se pudo ${isActive ? 'desactivar' : 'reactivar'} el alimento`, "error");
        }
    }
}

// Ver detalle (Modal simple)
async function viewFoodDetail(foodId) {
    const food = foods.value.find(f => f.id === foodId);
    if (!food) return;

    Swal.fire({
        title: food.nombre,
        html: `
            <div class="text-start">
                <p><strong>Calorías:</strong> ${food.kcal} kcal</p>
                <p><strong>Proteínas:</strong> ${food.proteinas} g</p>
                <p><strong>Carbohidratos:</strong> ${food.carbos} g</p>
                <p><strong>Costo por Unidad:</strong> ${formatCurrency(food.costo)}</p>
                <p><strong>Estado:</strong> ${food.activo ? '<span class="badge bg-success">Activo</span>' : '<span class="badge bg-danger">Inactivo</span>'}</p>
            </div>
        `,
        confirmButtonColor: "#4CAF50" // Verde
    });
}


// Carga inicial al montar el componente
onMounted(() => {
    loadFoods();
});
</script>

<template>
    <main class="flex-grow-1 p-4 bg-light">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3">Catalogo de Alimentos</h1>
                <p class="text-muted">Consulta la informacion nutricional y el costo unitario de cada alimento.</p>
            </div>
            <button v-if="isUserAdmin" class="btn btn-primary-nb" @click="showAddFoodModal">
                <i class="fas fa-plus me-1"></i> Agregar Alimento
            </button>
        </div>

        <div class="card p-4 card-shadow">
            <div v-if="isLoading" class="text-center p-5">
                <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
                <p class="mt-2 text-muted">Cargando catalogo...</p>
            </div>

            <div v-else-if="foods.length === 0" class="text-center p-5">
                 <p class="text-muted">No hay alimentos registrados{{ isUserAdmin ? '' : ' activos' }}.</p>
                 <button v-if="isUserAdmin" class="btn btn-primary-nb mt-3" @click="showAddFoodModal">
                    <i class="fas fa-plus me-1"></i> Agregar el Primer Alimento
                </button>
            </div>

            <div v-else class="table-responsive">
                <table class="table table-hover align-middle">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Calorías (kcal)</th>
                            <th>Proteínas (g)</th>
                            <th>Carbohidratos (g)</th>
                            <th>Costo Unitario</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody id="foodsTableBody">
                        <tr v-for="food in foods" :key="food.id" :class="{'table-secondary': !food.activo}">
                            <td>{{ food.nombre }}</td>
                            <td class="text-end">{{ food.kcal?.toFixed(1) ?? 'N/A' }}</td>
                            <td class="text-end">{{ food.proteinas?.toFixed(1) ?? 'N/A' }} g</td>
                            <td class="text-end">{{ food.carbos?.toFixed(1) ?? 'N/A' }} g</td>
                            <td class="text-end">{{ formatCurrency(food.costo) }}</td>
                            <td>
                                <span v-if="food.activo" class="badge bg-success">Activo</span>
                                <span v-else class="badge bg-danger">Inactivo</span>
                            </td>
                            <td>
                                <button class="btn btn-sm btn-outline-info me-1" title="Ver Detalle" @click="viewFoodDetail(food.id)">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <span v-if="isUserAdmin">
                                    <button class="btn btn-sm btn-outline-warning me-1" title="Editar" @click="showEditFoodModal(food.id)"><i class="fas fa-edit"></i></button>
                                    <button
                                        :class="['btn', 'btn-sm', food.activo ? 'btn-outline-danger' : 'btn-outline-secondary']"
                                        :title="food.activo ? 'Desactivar' : 'Reactivar'"
                                        @click="deleteFood(food.id)">
                                        <i :class="['fas', food.activo ? 'fa-trash-alt' : 'fa-undo']"></i>
                                    </button>
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
</template>

<style scoped>
/* Estilos adicionales si son necesarios */
.table td, .table th {
    vertical-align: middle;
}
.text-end {
    text-align: right;
}
</style>