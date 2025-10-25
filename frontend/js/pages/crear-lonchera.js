// crear-lonchera.js - Gestión de creación de loncheras con validación de restricciones

// ========================================
// VARIABLES GLOBALES
// ========================================

let foods = [];
let restrictions = [];
let currentLunchboxId = null;
let selectedChildId = null;
let lunchboxItems = [];

// ========================================
// INICIALIZACIÓN
// ========================================

document.addEventListener('DOMContentLoaded', async () => {
    // Verificar permisos
    if (!canUserDo('add_lunchbox')) {
        showUpgradeModal('Crear loncheras');
        setTimeout(() => {
            window.location.href = 'dashboard.html';
        }, 3000);
        return;
    }

    await loadChildren();
    await loadFoods();

    // Event listeners
    document.getElementById('hijoSelect').addEventListener('change', onChildChange);
    document.getElementById('saveLunchboxBtn').addEventListener('click', saveLunchbox);
});

// ========================================
// CARGAR DATOS
// ========================================

async function loadChildren() {
    try {
        showLoading('Cargando hijos...');
        const response = await API.get('/children');
        const children = await response.json();

        const select = document.getElementById('hijoSelect');
        select.innerHTML = '<option value="">Selecciona un hijo</option>';

        children.forEach(child => {
            const option = document.createElement('option');
            option.value = child.id;
            option.textContent = child.nombre;
            select.appendChild(option);
        });

        closeLoading();
    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudieron cargar los hijos', 'error');
    }
}

async function loadFoods() {
    try {
        showLoading('Cargando alimentos...');
        const response = await API.get('/foods');
        foods = await response.json();
        closeLoading();
    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudieron cargar los alimentos', 'error');
    }
}

async function loadRestrictions(childId) {
    try {
        const response = await API.get(`/restrictions?hijo_id=${childId}`);
        restrictions = await response.json();

        // Mostrar resumen de restricciones
        displayRestrictionsInfo();

        return restrictions;
    } catch (error) {
        console.error('Error al cargar restricciones:', error);
        restrictions = [];
        return [];
    }
}

// ========================================
// MANEJO DE CAMBIOS
// ========================================

async function onChildChange(event) {
    selectedChildId = event.target.value;

    if (!selectedChildId) {
        document.getElementById('foodsContainer').innerHTML = '';
        document.getElementById('restrictionsInfo').innerHTML = '';
        return;
    }

    // Cargar restricciones del hijo
    await loadRestrictions(selectedChildId);

    // Crear nueva lonchera
    await createLunchbox();

    // Renderizar alimentos
    renderFoods();
}

// ========================================
// CREAR LONCHERA
// ========================================

async function createLunchbox() {
    try {
        showLoading('Creando lonchera...');

        const today = new Date().toISOString().split('T')[0];

        const response = await API.post('/lunchboxes', {
            hijo_id: parseInt(selectedChildId),
            fecha: today,
            estado: 'Borrador'
        });

        const lunchbox = await response.json();
        currentLunchboxId = lunchbox.id;

        closeLoading();
        showNotification('Éxito', 'Lonchera creada', 'success');

    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudo crear la lonchera', 'error');
    }
}

// ========================================
// RENDERIZAR ALIMENTOS CON RESTRICCIONES
// ========================================

function renderFoods() {
    const container = document.getElementById('foodsContainer');

    if (foods.length === 0) {
        container.innerHTML = '<p style="color: var(--text-light);">No hay alimentos disponibles</p>';
        return;
    }

    container.innerHTML = foods.map(food => {
        // Verificar si está prohibido
        const restrictionCheck = checkFoodRestrictions(food);

        const cardStyle = restrictionCheck.isRestricted ?
            'opacity: 0.6; border: 2px solid #F44336;' : '';

        return `
            <div class="food-card" style="${cardStyle}">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <h4>
                            ${restrictionCheck.icon} ${food.nombre}
                            ${restrictionCheck.isRestricted ?
                                '<span class="badge" style="background: #F44336; color: white; font-size: 11px; padding: 2px 8px; border-radius: 4px;">PROHIBIDO</span>'
                                : ''}
                        </h4>
                        <p style="font-size: 13px; color: var(--text-light); margin: 4px 0;">
                            ${food.kcal} kcal | Prot: ${food.proteinas}g | Carbos: ${food.carbos}g
                        </p>
                        ${restrictionCheck.isRestricted ? `
                            <p style="color: #F44336; font-size: 12px; margin-top: 6px;">
                                <i class="fas fa-exclamation-circle"></i>
                                ${restrictionCheck.message}
                            </p>
                        ` : ''}
                    </div>
                    <button
                        class="btn ${restrictionCheck.isRestricted ? 'btn-danger' : 'btn-primary'}"
                        style="padding: 8px 16px; min-width: 100px;"
                        onclick="${restrictionCheck.isRestricted ? 'showRestrictionWarning' : 'addFoodToLunchbox'}(${food.id})"
                        ${restrictionCheck.isRestricted ? 'disabled' : ''}
                    >
                        <i class="fas ${restrictionCheck.isRestricted ? 'fa-ban' : 'fa-plus'}"></i>
                        ${restrictionCheck.isRestricted ? 'Prohibido' : 'Agregar'}
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

// ========================================
// VALIDACIÓN DE RESTRICCIONES
// ========================================

/**
 * Verifica si un alimento tiene restricciones
 * @param {Object} food - Objeto alimento
 * @returns {Object} { isRestricted: boolean, message: string, icon: string }
 */
function checkFoodRestrictions(food) {
    if (!restrictions || restrictions.length === 0) {
        return { isRestricted: false, message: '', icon: '' };
    }

    // Verificar alergia
    const allergy = restrictions.find(r =>
        r.tipo === 'alergia' && r.alimento_id === food.id
    );

    if (allergy) {
        return {
            isRestricted: true,
            message: 'Alergia registrada',
            icon: '🚫'
        };
    }

    // Verificar prohibido por texto
    const prohibited = restrictions.find(r => {
        if (r.tipo === 'prohibido' && r.texto) {
            const texto = r.texto.toLowerCase().trim();
            const nombre = food.nombre.toLowerCase();
            return nombre.includes(texto) || texto.includes(nombre);
        }
        return false;
    });

    if (prohibited) {
        return {
            isRestricted: true,
            message: `Contiene: ${prohibited.texto}`,
            icon: '⚠️'
        };
    }

    return { isRestricted: false, message: '', icon: '' };
}

/**
 * Muestra advertencia cuando se intenta agregar alimento prohibido
 */
function showRestrictionWarning(foodId) {
    const food = foods.find(f => f.id === foodId);
    const check = checkFoodRestrictions(food);

    Swal.fire({
        icon: 'error',
        title: 'Alimento Prohibido',
        html: `
            <p><strong>${food.nombre}</strong> no puede ser agregado a la lonchera.</p>
            <p style="color: #F44336; margin-top: 12px;">
                <i class="fas fa-exclamation-triangle"></i>
                ${check.message}
            </p>
            <p style="margin-top: 12px; font-size: 14px; color: var(--text-light);">
                Este alimento está en la lista de restricciones del niño.
            </p>
        `,
        confirmButtonColor: '#F44336',
        confirmButtonText: 'Entendido'
    });
}

// ========================================
// AGREGAR ALIMENTO A LONCHERA
// ========================================

async function addFoodToLunchbox(foodId) {
    // Validar permisos de personalización
    if (!canUserDo('customize_lunchbox')) {
        Swal.fire({
            icon: 'warning',
            title: 'Función Premium',
            html: `
                <p>La personalización alimento por alimento es una función <strong>Premium</strong>.</p>
                <p style="margin-top: 12px;">Tu plan actual: <strong>${getUserPlan()}</strong></p>
            `,
            showCancelButton: true,
            confirmButtonText: 'Ver Planes',
            cancelButtonText: 'Cancelar',
            confirmButtonColor: '#4CAF50'
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = 'planes.html';
            }
        });
        return;
    }

    if (!currentLunchboxId) {
        showNotification('Error', 'Primero debes seleccionar un hijo', 'warning');
        return;
    }

    const food = foods.find(f => f.id === foodId);

    // Doble verificación de restricciones (seguridad frontend)
    const check = checkFoodRestrictions(food);
    if (check.isRestricted) {
        showRestrictionWarning(foodId);
        return;
    }

    try {
        showLoading('Agregando alimento...');

        await API.post(`/lunchboxes/${currentLunchboxId}/items`, {
            alimento_id: foodId,
            cantidad: 1
        });

        closeLoading();
        showNotification('Éxito', `${food.nombre} agregado correctamente`, 'success');

        // Recargar items de la lonchera
        await loadLunchboxItems();

    } catch (error) {
        closeLoading();

        // Manejar error de restricción desde backend
        if (error.detail && error.detail.error === 'restriction_violation') {
            Swal.fire({
                icon: 'error',
                title: 'Restricción Violada',
                text: error.detail.message,
                confirmButtonColor: '#F44336'
            });
        } else {
            showNotification('Error', error.message || 'No se pudo agregar el alimento', 'error');
        }
    }
}

// ========================================
// CARGAR ITEMS DE LONCHERA
// ========================================

async function loadLunchboxItems() {
    if (!currentLunchboxId) return;

    try {
        const response = await API.get(`/lunchboxes/${currentLunchboxId}/items`);
        lunchboxItems = await response.json();

        renderLunchboxItems();
        calculateNutrition();

    } catch (error) {
        console.error('Error al cargar items:', error);
    }
}

function renderLunchboxItems() {
    const container = document.getElementById('lunchboxItemsContainer');

    if (lunchboxItems.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 40px; color: var(--text-light);">
                <i class="fas fa-apple-alt" style="font-size: 48px; opacity: 0.3;"></i>
                <p style="margin-top: 16px;">La lonchera está vacía</p>
                <p style="font-size: 14px;">Agrega alimentos desde el menú de la izquierda</p>
            </div>
        `;
        return;
    }

    container.innerHTML = lunchboxItems.map(item => {
        const food = foods.find(f => f.id === item.alimento_id);
        if (!food) return '';

        return `
            <div class="lunchbox-item">
                <div style="flex: 1;">
                    <h4>${food.nombre}</h4>
                    <p style="font-size: 13px; color: var(--text-light);">
                        Cantidad: ${item.cantidad} |
                        ${food.kcal * item.cantidad} kcal
                    </p>
                </div>
                <button
                    class="btn btn-danger btn-sm"
                    onclick="removeItemFromLunchbox(${item.alimento_id})"
                    style="padding: 6px 12px;"
                >
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
    }).join('');
}

// ========================================
// REMOVER ALIMENTO
// ========================================

async function removeItemFromLunchbox(foodId) {
    if (!canUserDo('customize_lunchbox')) {
        showNotification('Error', 'Solo usuarios Premium pueden quitar alimentos', 'warning');
        return;
    }

    const result = await Swal.fire({
        icon: 'question',
        title: '¿Quitar alimento?',
        text: '¿Estás seguro de quitar este alimento de la lonchera?',
        showCancelButton: true,
        confirmButtonText: 'Sí, quitar',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#F44336'
    });

    if (!result.isConfirmed) return;

    try {
        showLoading('Quitando alimento...');

        await API.delete(`/lunchboxes/${currentLunchboxId}/items/${foodId}`);

        closeLoading();
        showNotification('Éxito', 'Alimento quitado', 'success');

        await loadLunchboxItems();

    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudo quitar el alimento', 'error');
    }
}

// ========================================
// CALCULAR NUTRICIÓN
// ========================================

function calculateNutrition() {
    if (lunchboxItems.length === 0) {
        document.getElementById('nutritionSummary').innerHTML = `
            <p style="color: var(--text-light);">Agrega alimentos para ver el resumen nutricional</p>
        `;
        return;
    }

    let totalKcal = 0;
    let totalProteins = 0;
    let totalCarbs = 0;

    lunchboxItems.forEach(item => {
        const food = foods.find(f => f.id === item.alimento_id);
        if (food) {
            totalKcal += food.kcal * item.cantidad;
            totalProteins += food.proteinas * item.cantidad;
            totalCarbs += food.carbos * item.cantidad;
        }
    });

    document.getElementById('nutritionSummary').innerHTML = `
        <div class="nutrition-grid">
            <div class="nutrition-card">
                <h4>Calorías</h4>
                <p class="nutrition-value">${totalKcal.toFixed(0)}</p>
                <p class="nutrition-unit">kcal</p>
            </div>
            <div class="nutrition-card">
                <h4>Proteínas</h4>
                <p class="nutrition-value">${totalProteins.toFixed(1)}</p>
                <p class="nutrition-unit">g</p>
            </div>
            <div class="nutrition-card">
                <h4>Carbohidratos</h4>
                <p class="nutrition-value">${totalCarbs.toFixed(1)}</p>
                <p class="nutrition-unit">g</p>
            </div>
        </div>
    `;
}

// ========================================
// MOSTRAR INFO DE RESTRICCIONES
// ========================================

function displayRestrictionsInfo() {
    const container = document.getElementById('restrictionsInfo');

    if (!restrictions || restrictions.length === 0) {
        container.innerHTML = `
            <div class="alert alert-success">
                <i class="fas fa-check-circle"></i>
                Sin restricciones alimentarias
            </div>
        `;
        return;
    }

    const alergias = restrictions.filter(r => r.tipo === 'alergia');
    const prohibidos = restrictions.filter(r => r.tipo === 'prohibido');

    container.innerHTML = `
        <div class="restrictions-summary">
            ${alergias.length > 0 ? `
                <div class="alert alert-danger">
                    <strong><i class="fas fa-exclamation-triangle"></i> Alergias (${alergias.length}):</strong>
                    <ul style="margin: 8px 0 0 20px;">
                        ${alergias.map(a => {
                            const food = foods.find(f => f.id === a.alimento_id);
                            return `<li>${food ? food.nombre : 'Desconocido'}</li>`;
                        }).join('')}
                    </ul>
                </div>
            ` : ''}

            ${prohibidos.length > 0 ? `
                <div class="alert alert-warning">
                    <strong><i class="fas fa-ban"></i> Prohibidos (${prohibidos.length}):</strong>
                    <ul style="margin: 8px 0 0 20px;">
                        ${prohibidos.map(p => `<li>${p.texto}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
    `;
}

// ========================================
// GUARDAR LONCHERA
// ========================================

async function saveLunchbox() {
    if (!currentLunchboxId) {
        showNotification('Error', 'No hay lonchera para guardar', 'warning');
        return;
    }

    if (lunchboxItems.length === 0) {
        showNotification('Advertencia', 'La lonchera está vacía', 'warning');
        return;
    }

    try {
        showLoading('Guardando lonchera...');

        // Validar restricciones antes de confirmar
        const validateResponse = await API.post(`/lunchboxes/${currentLunchboxId}/validate`);
        const validation = await validateResponse.json();

        if (!validation.is_valid) {
            closeLoading();

            Swal.fire({
                icon: 'error',
                title: 'Restricciones Violadas',
                html: `
                    <p>La lonchera contiene alimentos prohibidos:</p>
                    <ul style="text-align: left; margin: 12px 0;">
                        ${validation.errors.map(err => `<li>${err}</li>`).join('')}
                    </ul>
                `,
                confirmButtonColor: '#F44336'
            });
            return;
        }

        // Actualizar estado a "Confirmada"
        await API.patch(`/lunchboxes/${currentLunchboxId}`, {
            estado: 'Confirmada'
        });

        closeLoading();

        Swal.fire({
            icon: 'success',
            title: '¡Lonchera guardada!',
            text: 'La lonchera ha sido confirmada exitosamente',
            confirmButtonText: 'Ver mis loncheras'
        }).then(() => {
            window.location.href = 'mis-loncheras.html';
        });

    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudo guardar la lonchera', 'error');
    }
}