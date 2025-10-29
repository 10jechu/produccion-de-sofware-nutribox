<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { isAdmin, getUserDetail } from '@/utils/user';
import authService from '@/services/auth.service';

const foods = ref([]);
const predeterminedMenus = ref([]);
const isLoadingFoods = ref(true);
const isLoadingMenus = ref(true);
const isUserAdmin = computed(() => isAdmin());
const adminUserId = computed(() => getUserDetail()?.id);

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const parts = dateString.split('-');
    const date = new Date(Date.UTC(parts[0], parts[1] - 1, parts[2]));
    return date.toLocaleDateString('es-CO', { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' });
}

function formatCurrency(value) {
    const numberValue = Number(value);
    if (isNaN(numberValue)) return '$ 0';
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(numberValue);
}

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

async function loadPredeterminedMenus() {
    isLoadingMenus.value = true;
    if (!isUserAdmin.value) { isLoadingMenus.value = false; return; }
    try {
        predeterminedMenus.value = await apiService.get('/menus-predeterminados');
        isLoadingMenus.value = false;
    } catch (error) {
        isLoadingMenus.value = false;
        console.error("Error cargando menús predeterminados:", error);
        Swal.fire('Error', 'No se pudieron cargar los menús predeterminados.', 'error');
    }
}

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

const showAddPredeterminedMenuModal = async () => {
    const { value: formValues } = await Swal.fire({
        title: "Crear Nuevo Menú Predeterminado",
        html: `
            <input id="swal-menu-nombre" class="swal2-input form-control" placeholder="Nombre del Menú (ej: Lunes Saludable)" required>
            <textarea id="swal-menu-desc" class="swal2-input form-control" placeholder="Descripción corta (opcional)"></textarea>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: "#4CAF50",
        cancelButtonColor: "#DC3545",
        confirmButtonText: "Crear y Añadir Alimentos",
        cancelButtonText: "Cancelar",
        preConfirm: () => {
            const nombre = document.getElementById("swal-menu-nombre").value;
            const descripcion = document.getElementById("swal-menu-desc").value;
            if (!nombre) {
                Swal.showValidationMessage("El nombre es requerido."); return false;
            }
            return { nombre, descripcion };
        }
    });

    if (formValues) {
        try {
            Swal.fire({ title: 'Creando menú...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });
            const newMenu = await apiService.post('/menus-predeterminados', formValues);
            Swal.close();
            Swal.fire('¡Éxito!', 'Menú creado. Ahora añade alimentos.', 'success');
            await loadPredeterminedMenus();
            showEditPredeterminedMenuItemsModal(newMenu);
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'No se pudo crear el menú.', 'error');
        }
    }
};

const showEditPredeterminedMenuItemsModal = async (menu) => {
    if (foods.value.length === 0) await loadFoods();

    let currentMenu = menu; // Variable para mantener el estado actualizado del menú

    const buildModalHtml = (menuData) => {
        let itemsHtml = menuData.items && menuData.items.length > 0
            ? menuData.items.map(item => `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    ${item.alimento?.nombre || `Alimento ID ${item.alimento_id}`} (x${item.cantidad})
                    <button class="btn btn-sm btn-outline-danger btn-remove-item" data-alimento-id="${item.alimento_id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </li>`).join('')
            : '<li class="list-group-item text-muted">Aún no hay alimentos.</li>';

        const foodOptions = foods.value.filter(f => f.activo).map(f => `<option value="${f.id}">${f.nombre}</option>`).join('');

        return `
            <h5>Alimentos Actuales</h5>
            <ul class="list-group list-group-flush mb-3" id="current-items">${itemsHtml}</ul>
            <hr>
            <h5>Añadir Alimento</h5>
            <div class="input-group mb-3">
                <select id="swal-select-food" class="form-select">
                    <option value="">Selecciona un alimento...</option>
                    ${foodOptions}
                </select>
                <input id="swal-quantity" type="number" class="form-control" value="1" min="1" style="max-width: 80px;">
                <button class="btn btn-success" id="swal-add-item-btn">Añadir</button>
            </div>
        `;
    }

    const swalInstance = await Swal.fire({
        title: `Editar Items: ${menu.nombre}`,
        html: buildModalHtml(currentMenu),
        showCancelButton: true,
        showConfirmButton: false,
        cancelButtonText: 'Cerrar',
        width: '600px',
        didOpen: (modal) => {
            const addItemHandler = async () => {
                const alimentoId = modal.querySelector('#swal-select-food').value;
                const cantidad = parseInt(modal.querySelector('#swal-quantity').value) || 1;
                if (!alimentoId) return;

                try {
                    Swal.showLoading();
                    await apiService.post(`/menus-predeterminados/${currentMenu.id}/items`, { alimento_id: parseInt(alimentoId), cantidad });
                    currentMenu = await apiService.get(`/menus-predeterminados/${currentMenu.id}`); // Recarga
                    Swal.update({ html: buildModalHtml(currentMenu) }); // Actualiza HTML del modal
                    Swal.hideLoading();
                    loadPredeterminedMenus(); // Recarga tabla principal en fondo
                } catch (error) {
                    Swal.showValidationMessage(error.message || 'Error al añadir item.');
                }
            };

            const removeItemHandler = async (event) => {
                const button = event.target.closest('.btn-remove-item');
                if (!button) return;
                const alimentoIdToRemove = button.getAttribute('data-alimento-id');
                 if (!alimentoIdToRemove) return;

                try {
                    Swal.showLoading();
                    await apiService.delete(`/menus-predeterminados/${currentMenu.id}/items/${alimentoIdToRemove}`);
                    currentMenu = await apiService.get(`/menus-predeterminados/${currentMenu.id}`); // Recarga
                    Swal.update({ html: buildModalHtml(currentMenu) }); // Actualiza HTML
                    Swal.hideLoading();
                    loadPredeterminedMenus(); // Recarga tabla principal en fondo
                } catch (error) {
                    Swal.showValidationMessage(error.message || 'Error al quitar item.');
                }
            };

            modal.querySelector('#swal-add-item-btn').addEventListener('click', addItemHandler);
            modal.querySelector('#current-items').addEventListener('click', removeItemHandler);

            // Guardar referencias para limpiar al cerrar
            modal.addItemHandler = addItemHandler;
            modal.removeItemHandler = removeItemHandler;
        },
        willClose: (modal) => {
            // Limpiar listeners al cerrar el modal
            if (modal && modal.querySelector('#swal-add-item-btn') && modal.addItemHandler) {
               modal.querySelector('#swal-add-item-btn').removeEventListener('click', modal.addItemHandler);
            }
             if (modal && modal.querySelector('#current-items') && modal.removeItemHandler) {
               modal.querySelector('#current-items').removeEventListener('click', modal.removeItemHandler);
            }
        }
    });
};

const deletePredeterminedMenu = async (id) => {
    const result = await Swal.fire({
        title: "¿Eliminar Menú Predeterminado?",
        text: "Esta acción eliminará la plantilla de menú permanentemente.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#DC3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Sí, Eliminar',
        cancelButtonText: 'Cancelar'
    });

    if (result.isConfirmed) {
        try {
            Swal.fire({ title: 'Eliminando...', allowOutsideClick: false, didOpen: () => Swal.showLoading() });
            await apiService.delete('/menus-predeterminados/' + id);
            Swal.close();
            Swal.fire('¡Éxito!', 'Menú predeterminado eliminado.', 'success');
            await loadPredeterminedMenus();
        } catch (error) {
            Swal.close();
            Swal.fire('Error', error.message || 'No se pudo eliminar el menú.', 'error');
        }
    }
};

onMounted(() => {
    loadFoods();
    loadPredeterminedMenus();
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
      <div class="card p-4 card-shadow mb-5">
          <div v-if="isLoadingFoods" class="text-center p-5">
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
                  <p class="text-muted">Crear y gestionar las plantillas de menú para usuarios.</p>
              </div>
               <button class="btn btn-success" @click="showAddPredeterminedMenuModal">
                  <i class="fas fa-plus me-1"></i> Crear Nuevo Menú
              </button>
          </div>

          <div v-if="isLoadingMenus" class="text-center p-5">
              <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
              <p class="mt-2 text-muted">Cargando menús predeterminados...</p>
          </div>
          <div v-else-if="predeterminedMenus.length === 0" class="text-center p-5 text-muted">
              No hay menús predeterminados creados. ¡Crea el primero!
          </div>
          <div v-else class="table-responsive">
              <table class="table table-hover align-middle">
                  <thead>
                      <tr>
                          <th>ID</th>
                          <th>Nombre</th>
                          <th>Descripción</th>
                          <th>Nº Items</th>
                          <th>Acciones</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="menu in predeterminedMenus" :key="menu.id">
                          <td>#{{ menu.id }}</td>
                          <td><strong>{{ menu.nombre }}</strong></td>
                          <td>{{ menu.descripcion || '-' }}</td>
                          <td>{{ menu.items?.length || 0 }}</td>
                          <td>
                              <button class="btn btn-sm btn-outline-primary me-1" @click="showEditPredeterminedMenuItemsModal(menu)" title="Editar Items">
                                  <i class="fas fa-pencil-alt"></i> Items
                              </button>
                              <button class="btn btn-sm btn-outline-danger" @click="deletePredeterminedMenu(menu.id)" title="Eliminar Menú">
                                  <i class="fas fa-trash"></i>
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
