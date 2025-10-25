// alimentos.js - Gestión de alimentos con control de permisos

// ========================================
// VARIABLES GLOBALES
// ========================================

let foods = [];
let currentPage = 1;
const itemsPerPage = 10;

// ========================================
// INICIALIZACIÓN
// ========================================

document.addEventListener('DOMContentLoaded', async () => {
    await loadFoods();
    renderActionButtons();

    // Event listeners
    document.getElementById('searchInput')?.addEventListener('input', filterFoods);
});

// ========================================
// RENDERIZAR BOTONES DE ACCIÓN
// ========================================

function renderActionButtons() {
    const container = document.getElementById('foodActions');

    if (!container) return;

    if (canUserDo('create_food')) {
        container.innerHTML = `
            <button class="btn btn-primary" onclick="showCreateFoodModal()">
                <i class="fas fa-plus"></i> Crear Alimento
            </button>
        `;
    } else {
        container.innerHTML = `
            <div class="alert alert-warning" style="max-width: 600px;">
                <div style="display: flex; align-items: center; gap: 16px;">
                    <i class="fas fa-lock" style="font-size: 32px; color: #FF9800;"></i>
                    <div style="flex: 1;">
                        <strong>Función Premium</strong>
                        <p style="margin: 4px 0 0 0; font-size: 14px;">
                            Actualiza a Premium para crear y gestionar alimentos personalizados
                        </p>
                    </div>
                    <button class="btn btn-outline" onclick="showUpgradeModal('Gestionar alimentos')">
                        Ver Planes
                    </button>
                </div>
            </div>
        `;
    }
}

// ========================================
// CARGAR ALIMENTOS
// ========================================

async function loadFoods(onlyActive = 'true') {
    try {
        showLoading('Cargando alimentos...');

        const response = await API.get(`/foods?only_active=${onlyActive}`);
        foods = await response.json();

        closeLoading();
        renderFoods();

    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudieron cargar los alimentos', 'error');
    }
}

// ========================================
// RENDERIZAR ALIMENTOS
// ========================================

function renderFoods() {
    const container = document.getElementById('foodsContainer');

    if (!container) return;

    if (foods.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 60px; color: var(--text-light);">
                <i class="fas fa-apple-alt" style="font-size: 64px; opacity: 0.3;"></i>
                <p style="margin-top: 16px; font-size: 18px;">No hay alimentos disponibles</p>
                ${canUserDo('create_food') ?
                    '<button class="btn btn-primary" onclick="showCreateFoodModal()" style="margin-top: 16px;">Crear Primer Alimento</button>'
                    : ''}
            </div>
        `;
        return;
    }

    container.innerHTML = `
        <div class="table-responsive">
            <table class="table">
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Calorías (kcal)</th>
                        <th>Proteínas (g)</th>
                        <th>Carbohidratos (g)</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    ${foods.map(food => `
                        <tr>
                            <td>
                                <strong>${food.nombre}</strong>
                            </td>
                            <td>${food.kcal}</td>
                            <td>${food.proteinas}</td>
                            <td>${food.carbos}</td>
                            <td>
                                <span class="badge ${food.activo ? 'badge-success' : 'badge-danger'}">
                                    ${food.activo ? 'Activo' : 'Inactivo'}
                                </span>
                            </td>
                            <td>
                                ${renderFoodActions(food)}
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

function renderFoodActions(food) {
    const canManage = canUserDo('edit_food');

    if (!canManage) {
        return `
            <button class="btn btn-sm btn-secondary" disabled title="Solo Premium puede editar">
                <i class="fas fa-lock"></i>
            </button>
        `;
    }

    return `
        <div style="display: flex; gap: 8px;">
            <button
                class="btn btn-sm btn-primary"
                onclick="showEditFoodModal(${food.id})"
                title="Editar"
            >
                <i class="fas fa-edit"></i>
            </button>
            <button
                class="btn btn-sm ${food.activo ? 'btn-danger' : 'btn-success'}"
                onclick="toggleFoodStatus(${food.id})"
                title="${food.activo ? 'Desactivar' : 'Activar'}"
            >
                <i class="fas fa-${food.activo ? 'times' : 'check'}"></i>
            </button>
        </div>
    `;
}

// ========================================
// CREAR ALIMENTO
// ========================================

function showCreateFoodModal() {
    if (!canUserDo('create_food')) {
        showUpgradeModal('Crear alimentos');
        return;
    }

    Swal.fire({
        title: 'Crear Nuevo Alimento',
        html: `
            <div style="text-align: left;">
                <div class="form-group">
                    <label>Nombre *</label>
                    <input type="text" id="foodName" class="swal2-input" placeholder="Ej: Manzana">
                </div>

                <div class="form-group">
                    <label>Calorías (kcal) *</label>
                    <input type="number" id="foodKcal" class="swal2-input" placeholder="Ej: 52" step="0.1">
                </div>

                <div class="form-group">
                    <label>Proteínas (g) *</label>
                    <input type="number" id="foodProteins" class="swal2-input" placeholder="Ej: 0.3" step="0.1">
                </div>

                <div class="form-group">
                    <label>Carbohidratos (g) *</label>
                    <input type="number" id="foodCarbs" class="swal2-input" placeholder="Ej: 14" step="0.1">
                </div>
            </div>
        `,
        showCancelButton: true,
        confirmButtonText: 'Crear',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#4CAF50',
        width: 500,
        preConfirm: () => {
            const nombre = document.getElementById('foodName').value.trim();
            const kcal = parseFloat(document.getElementById('foodKcal').value);
            const proteinas = parseFloat(document.getElementById('foodProteins').value);
            const carbos = parseFloat(document.getElementById('foodCarbs').value);

            if (!nombre) {
                Swal.showValidationMessage('El nombre es requerido');
                return false;
            }

            if (isNaN(kcal) || kcal < 0) {
                Swal.showValidationMessage('Las calorías deben ser un número positivo');
                return false;
            }

            if (isNaN(proteinas) || proteinas < 0) {
                Swal.showValidationMessage('Las proteínas deben ser un número positivo');
                return false;
            }

            if (isNaN(carbos) || carbos < 0) {
                Swal.showValidationMessage('Los carbohidratos deben ser un número positivo');
                return false;
            }

            return { nombre, kcal, proteinas, carbos };
        }
    }).then(async (result) => {
        if (result.isConfirmed && result.value) {
            await createFood(result.value);
        }
    });
}

async function createFood(data) {
    try {
        showLoading('Creando alimento...');

        await API.post('/foods', data);

        closeLoading();
        showNotification('Éxito', 'Alimento creado correctamente', 'success');

        await loadFoods();

    } catch (error) {
        closeLoading();

        if (error.detail && error.detail.includes('existe')) {
            showNotification('Error', 'Ya existe un alimento con ese nombre', 'error');
        } else if (error.status === 403) {
            showNotification('Error', 'No tienes permisos para crear alimentos', 'error');
        } else {
            showNotification('Error', 'No se pudo crear el alimento', 'error');
        }
    }
}

// ========================================
// EDITAR ALIMENTO
// ========================================

function showEditFoodModal(foodId) {
    if (!canUserDo('edit_food')) {
        showUpgradeModal('Editar alimentos');
        return;
    }

    const food = foods.find(f => f.id === foodId);
    if (!food) return;

    Swal.fire({
        title: 'Editar Alimento',
        html: `
            <div style="text-align: left;">
                <div class="form-group">
                    <label>Nombre *</label>
                    <input type="text" id="foodName" class="swal2-input" value="${food.nombre}">
                </div>

                <div class="form-group">
                    <label>Calorías (kcal) *</label>
                    <input type="number" id="foodKcal" class="swal2-input" value="${food.kcal}" step="0.1">
                </div>

                <div class="form-group">
                    <label>Proteínas (g) *</label>
                    <input type="number" id="foodProteins" class="swal2-input" value="${food.proteinas}" step="0.1">
                </div>

                <div class="form-group">
                    <label>Carbohidratos (g) *</label>
                    <input type="number" id="foodCarbs" class="swal2-input" value="${food.carbos}" step="0.1">
                </div>
            </div>
        `,
        showCancelButton: true,
        confirmButtonText: 'Guardar',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#4CAF50',
        width: 500,
        preConfirm: () => {
            const nombre = document.getElementById('foodName').value.trim();
            const kcal = parseFloat(document.getElementById('foodKcal').value);
            const proteinas = parseFloat(document.getElementById('foodProteins').value);
            const carbos = parseFloat(document.getElementById('foodCarbs').value);

            if (!nombre) {
                Swal.showValidationMessage('El nombre es requerido');
                return false;
            }

            if (isNaN(kcal) || kcal < 0) {
                Swal.showValidationMessage('Las calorías deben ser un número positivo');
                return false;
            }

            if (isNaN(proteinas) || proteinas < 0) {
                Swal.showValidationMessage('Las proteínas deben ser un número positivo');
                return false;
            }

            if (isNaN(carbos) || carbos < 0) {
                Swal.showValidationMessage('Los carbohidratos deben ser un número positivo');
                return false;
            }

            return { nombre, kcal, proteinas, carbos };
        }
    }).then(async (result) => {
        if (result.isConfirmed && result.value) {
            await updateFood(foodId, result.value);
        }
    });
}

async function updateFood(foodId, data) {
    try {
        showLoading('Actualizando alimento...');

        await API.patch(`/foods/${foodId}`, data);

        closeLoading();
        showNotification('Éxito', 'Alimento actualizado correctamente', 'success');

        await loadFoods();

    } catch (error) {
        closeLoading();

        if (error.status === 403) {
            showNotification('Error', 'No tienes permisos para editar alimentos', 'error');
        } else {
            showNotification('Error', 'No se pudo actualizar el alimento', 'error');
        }
    }
}

// ========================================
// ACTIVAR/DESACTIVAR ALIMENTO
// ========================================

async function toggleFoodStatus(foodId) {
    if (!canUserDo('delete_food')) {
        showUpgradeModal('Gestionar estado de alimentos');
        return;
    }

    const food = foods.find(f => f.id === foodId);
    if (!food) return;

    const action = food.activo ? 'desactivar' : 'activar';

    const result = await Swal.fire({
        icon: 'question',
        title: `¿${action.charAt(0).toUpperCase() + action.slice(1)} alimento?`,
        text: `¿Estás seguro de ${action} "${food.nombre}"?`,
        showCancelButton: true,
        confirmButtonText: `Sí, ${action}`,
        cancelButtonText: 'Cancelar',
        confirmButtonColor: food.activo ? '#F44336' : '#4CAF50'
    });

    if (!result.isConfirmed) return;

    try {
        showLoading(`${action === 'desactivar' ? 'Desactivando' : 'Activando'} alimento...`);

        if (food.activo) {
            await API.delete(`/foods/${foodId}`);
        } else {
            // Para reactivar, necesitarías un endpoint PATCH que cambie el estado
            await API.patch(`/foods/${foodId}`, { activo: true });
        }

        closeLoading();
        showNotification('Éxito', `Alimento ${action === 'desactivar' ? 'desactivado' : 'activado'} correctamente`, 'success');

        await loadFoods();

    } catch (error) {
        closeLoading();

        if (error.status === 403) {
            showNotification('Error', 'No tienes permisos para cambiar el estado de alimentos', 'error');
        } else {
            showNotification('Error', `No se pudo ${action} el alimento`, 'error');
        }
    }
}

// ========================================
// FILTRAR ALIMENTOS
// ========================================

function filterFoods() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();

    const filtered = foods.filter(food =>
        food.nombre.toLowerCase().includes(searchTerm)
    );

    // Renderizar solo los filtrados (temporal simple)
    const container = document.getElementById('foodsContainer');

    if (filtered.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 40px; color: var(--text-light);">
                <i class="fas fa-search" style="font-size: 48px; opacity: 0.3;"></i>
                <p style="margin-top: 16px;">No se encontraron alimentos</p>
            </div>
        `;
        return;
    }

    // Reutilizar lógica de renderizado (puedes mejorar esto)
    const originalFoods = [...foods];
    foods = filtered;
    renderFoods();
    foods = originalFoods;
}

// ========================================
// FILTRO POR ESTADO
// ========================================

function filterByStatus(status) {
    let filter = 'true';

    if (status === 'inactive') {
        filter = 'false';
    } else if (status === 'all') {
        filter = 'all';
    }

    loadFoods(filter);
}