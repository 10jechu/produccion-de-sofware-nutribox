// restricciones.js - Gestión de restricciones alimentarias

// ========================================
// VARIABLES GLOBALES
// ========================================

let restrictions = [];
let children = [];
let foods = [];
let selectedChildId = null;

// ========================================
// INICIALIZACIÓN
// ========================================

document.addEventListener('DOMContentLoaded', async () => {
    // Verificar permisos
    if (!canUserDo('configure_restrictions')) {
        showUpgradeModal('Configurar restricciones alimentarias');
        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 3000);
        return;
    }

    await loadChildren();
    await loadFoods();

    // Event listeners
    document.getElementById('childSelect')?.addEventListener('change', onChildChange);
    document.getElementById('addRestrictionBtn')?.addEventListener('click', showAddRestrictionModal);
});

// ========================================
// CARGAR DATOS
// ========================================

async function loadChildren() {
    try {
        showLoading('Cargando hijos...');
        const response = await API.get('/children');
        children = await response.json();

        const select = document.getElementById('childSelect');
        if (select) {
            select.innerHTML = '<option value="">Selecciona un hijo</option>';
            children.forEach(child => {
                const option = document.createElement('option');
                option.value = child.id;
                option.textContent = child.nombre;
                select.appendChild(option);
            });
        }

        closeLoading();
    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudieron cargar los hijos', 'error');
    }
}

async function loadFoods() {
    try {
        const response = await API.get('/foods?only_active=true');
        foods = await response.json();
    } catch (error) {
        console.error('Error al cargar alimentos:', error);
        foods = [];
    }
}

async function loadRestrictions(childId) {
    try {
        showLoading('Cargando restricciones...');
        const response = await API.get(`/restrictions?hijo_id=${childId}`);
        restrictions = await response.json();
        closeLoading();
        renderRestrictions();
    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudieron cargar las restricciones', 'error');
    }
}

// ========================================
// EVENTOS
// ========================================

async function onChildChange(event) {
    selectedChildId = event.target.value;

    if (!selectedChildId) {
        document.getElementById('restrictionsContainer').innerHTML = '';
        return;
    }

    await loadRestrictions(selectedChildId);
}

// ========================================
// RENDERIZAR RESTRICCIONES
// ========================================

function renderRestrictions() {
    const container = document.getElementById('restrictionsContainer');

    if (!container) return;

    if (!selectedChildId) {
        container.innerHTML = `
            <div style="text-align: center; padding: 40px; color: var(--text-light);">
                <i class="fas fa-child" style="font-size: 48px; opacity: 0.3;"></i>
                <p style="margin-top: 16px;">Selecciona un hijo para ver sus restricciones</p>
            </div>
        `;
        return;
    }

    const child = children.find(c => c.id == selectedChildId);

    const alergias = restrictions.filter(r => r.tipo === 'alergia');
    const prohibidos = restrictions.filter(r => r.tipo === 'prohibido');

    container.innerHTML = `
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                <h2>${child ? child.nombre : 'Hijo'}</h2>
                <button class="btn btn-primary" onclick="showAddRestrictionModal()">
                    <i class="fas fa-plus"></i> Agregar Restricción
                </button>
            </div>

            <!-- RESUMEN -->
            <div class="restrictions-summary" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 32px;">
                <div class="stat-card" style="background: #FFEBEE; border-left: 4px solid #F44336;">
                    <h3 style="color: #F44336; margin: 0;">Alergias</h3>
                    <p style="font-size: 32px; font-weight: bold; margin: 8px 0; color: #F44336;">${alergias.length}</p>
                </div>
                <div class="stat-card" style="background: #FFF3E0; border-left: 4px solid #FF9800;">
                    <h3 style="color: #FF9800; margin: 0;">Prohibidos</h3>
                    <p style="font-size: 32px; font-weight: bold; margin: 8px 0; color: #FF9800;">${prohibidos.length}</p>
                </div>
                <div class="stat-card" style="background: #E8F5E9; border-left: 4px solid #4CAF50;">
                    <h3 style="color: #4CAF50; margin: 0;">Total</h3>
                    <p style="font-size: 32px; font-weight: bold; margin: 8px 0; color: #4CAF50;">${restrictions.length}</p>
                </div>
            </div>

            <!-- ALERGIAS -->
            <div class="restrictions-section" style="margin-bottom: 32px;">
                <h3 style="color: #F44336; display: flex; align-items: center; gap: 8px;">
                    <i class="fas fa-exclamation-triangle"></i>
                    Alergias (${alergias.length})
                </h3>

                ${alergias.length === 0 ? `
                    <p style="color: var(--text-light); padding: 20px; background: #F5F5F5; border-radius: 8px;">
                        Sin alergias registradas
                    </p>
                ` : `
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; margin-top: 16px;">
                        ${alergias.map(a => {
                            const food = foods.find(f => f.id === a.alimento_id);
                            return `
                                <div class="restriction-card" style="border-left: 4px solid #F44336;">
                                    <div style="display: flex; justify-content: space-between; align-items: start;">
                                        <div style="flex: 1;">
                                            <h4 style="margin: 0 0 8px 0; color: #F44336;">
                                                ${food ? food.nombre : 'Alimento desconocido'}
                                            </h4>
                                            <p style="font-size: 13px; color: var(--text-light); margin: 0;">
                                                <i class="fas fa-tag"></i> Alergia
                                            </p>
                                        </div>
                                        <button
                                            class="btn btn-danger btn-sm"
                                            onclick="deleteRestriction(${a.id})"
                                            style="padding: 6px 12px;"
                                        >
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </div>
                            `;
                        }).join('')}
                    </div>
                `}
            </div>

            <!-- PROHIBIDOS -->
            <div class="restrictions-section">
                <h3 style="color: #FF9800; display: flex; align-items: center; gap: 8px;">
                    <i class="fas fa-ban"></i>
                    Alimentos Prohibidos (${prohibidos.length})
                </h3>

                ${prohibidos.length === 0 ? `
                    <p style="color: var(--text-light); padding: 20px; background: #F5F5F5; border-radius: 8px;">
                        Sin prohibiciones registradas
                    </p>
                ` : `
                    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; margin-top: 16px;">
                        ${prohibidos.map(p => `
                            <div class="restriction-card" style="border-left: 4px solid #FF9800;">
                                <div style="display: flex; justify-content: space-between; align-items: start;">
                                    <div style="flex: 1;">
                                        <h4 style="margin: 0 0 8px 0; color: #FF9800;">
                                            "${p.texto}"
                                        </h4>
                                        <p style="font-size: 13px; color: var(--text-light); margin: 0;">
                                            Se bloquean alimentos que contengan este término
                                        </p>
                                    </div>
                                    <button
                                        class="btn btn-danger btn-sm"
                                        onclick="deleteRestriction(${p.id})"
                                        style="padding: 6px 12px;"
                                    >
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                `}
            </div>
        </div>
    `;
}

// ========================================
// AGREGAR RESTRICCIÓN
// ========================================

function showAddRestrictionModal() {
    if (!selectedChildId) {
        showNotification('Advertencia', 'Primero selecciona un hijo', 'warning');
        return;
    }

    Swal.fire({
        title: 'Agregar Restricción',
        html: `
            <div style="text-align: left;">
                <div class="form-group">
                    <label><strong>Tipo de restricción *</strong></label>
                    <select id="restrictionType" class="swal2-input" onchange="toggleRestrictionFields()">
                        <option value="">Selecciona un tipo</option>
                        <option value="alergia">Alergia (alimento específico)</option>
                        <option value="prohibido">Prohibido (por texto)</option>
                    </select>
                </div>

                <div id="foodField" class="form-group" style="display: none;">
                    <label>Alimento *</label>
                    <select id="foodSelect" class="swal2-input">
                        <option value="">Selecciona un alimento</option>
                        ${foods.map(f => `<option value="${f.id}">${f.nombre}</option>`).join('')}
                    </select>
                    <small style="color: var(--text-light);">
                        El niño es alérgico a este alimento y será bloqueado automáticamente
                    </small>
                </div>

                <div id="textField" class="form-group" style="display: none;">
                    <label>Texto a buscar *</label>
                    <input type="text" id="restrictionText" class="swal2-input" placeholder="Ej: chocolate, maní, lácteos">
                    <small style="color: var(--text-light);">
                        Se bloquearán todos los alimentos que contengan este texto en su nombre
                    </small>
                </div>
            </div>
        `,
        showCancelButton: true,
        confirmButtonText: 'Agregar',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#4CAF50',
        width: 600,
        preConfirm: () => {
            const tipo = document.getElementById('restrictionType').value;

            if (!tipo) {
                Swal.showValidationMessage('Selecciona un tipo de restricción');
                return false;
            }

            if (tipo === 'alergia') {
                const alimentoId = document.getElementById('foodSelect').value;
                if (!alimentoId) {
                    Swal.showValidationMessage('Selecciona un alimento');
                    return false;
                }
                return {
                    tipo: 'alergia',
                    alimento_id: parseInt(alimentoId),
                    hijo_id: parseInt(selectedChildId)
                };
            } else {
                const texto = document.getElementById('restrictionText').value.trim();
                if (!texto) {
                    Swal.showValidationMessage('Ingresa un texto');
                    return false;
                }
                return {
                    tipo: 'prohibido',
                    texto: texto,
                    hijo_id: parseInt(selectedChildId)
                };
            }
        }
    }).then(async (result) => {
        if (result.isConfirmed && result.value) {
            await addRestriction(result.value);
        }
    });
}

// Función helper para toggle de campos
window.toggleRestrictionFields = function() {
    const tipo = document.getElementById('restrictionType').value;
    const foodField = document.getElementById('foodField');
    const textField = document.getElementById('textField');

    if (tipo === 'alergia') {
        foodField.style.display = 'block';
        textField.style.display = 'none';
    } else if (tipo === 'prohibido') {
        foodField.style.display = 'none';
        textField.style.display = 'block';
    } else {
        foodField.style.display = 'none';
        textField.style.display = 'none';
    }
};

async function addRestriction(data) {
    try {
        showLoading('Agregando restricción...');

        await API.post('/restrictions', data);

        closeLoading();
        showNotification('Éxito', 'Restricción agregada correctamente', 'success');

        await loadRestrictions(selectedChildId);

    } catch (error) {
        closeLoading();

        if (error.status === 403) {
            showNotification('Error', 'No tienes permisos para configurar restricciones', 'error');
        } else {
            showNotification('Error', 'No se pudo agregar la restricción', 'error');
        }
    }
}

// ========================================
// ELIMINAR RESTRICCIÓN
// ========================================

async function deleteRestriction(restrictionId) {
    const result = await Swal.fire({
        icon: 'question',
        title: '¿Eliminar restricción?',
        text: '¿Estás seguro de eliminar esta restricción?',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#F44336'
    });

    if (!result.isConfirmed) return;

    try {
        showLoading('Eliminando restricción...');

        await API.delete(`/restrictions/${restrictionId}`);

        closeLoading();
        showNotification('Éxito', 'Restricción eliminada correctamente', 'success');

        await loadRestrictions(selectedChildId);

    } catch (error) {
        closeLoading();

        if (error.status === 403) {
            showNotification('Error', 'No tienes permisos para eliminar restricciones', 'error');
        } else {
            showNotification('Error', 'No se pudo eliminar la restricción', 'error');
        }
    }
}