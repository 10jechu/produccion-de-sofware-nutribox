requireAuth();

let hijos = [];
let restricciones = [];
let alimentos = [];
let currentHijoId = null;

// Cargar datos iniciales
async function loadInitialData() {
    try {
        showLoading();
        const user = getUser();
        
        // Cargar hijos y alimentos en paralelo
        [hijos, alimentos] = await Promise.all([
            API.getChildren(user.id),
            API.getFoods('true')
        ]);
        
        populateHijosSelect();
        closeLoading();
        
        if (hijos.length === 0) {
            showNoChildrenMessage();
        }
    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudieron cargar los datos iniciales', 'error');
    }
}

function populateHijosSelect() {
    const select = document.getElementById('hijoSelect');
    select.innerHTML = '<option value="">-- Selecciona un hijo --</option>' +
        hijos.map(h => `<option value="${h.id}">${h.nombre}</option>`).join('');
}

function showNoChildrenMessage() {
    const container = document.getElementById('restrictionsContainer');
    container.innerHTML = `
        <div class="card" style="text-align: center; padding: 60px;">
            <i class="fas fa-child" style="font-size: 64px; color: var(--primary); margin-bottom: 16px;"></i>
            <h3>No tienes hijos registrados</h3>
            <p style="color: var(--text-light); margin-bottom: 24px;">
                Primero debes agregar un hijo para gestionar sus restricciones
            </p>
            <a href="hijos.html" class="btn btn-primary">
                <i class="fas fa-plus"></i> Ir a Mis Hijos
            </a>
        </div>
    `;
}

// Cargar restricciones del hijo seleccionado
async function loadRestrictions() {
    const hijoId = document.getElementById('hijoSelect').value;
    const btnAdd = document.getElementById('btnAddRestriction');
    
    if (!hijoId) {
        currentHijoId = null;
        btnAdd.disabled = true;
        const container = document.getElementById('restrictionsContainer');
        container.innerHTML = `
            <div class="card" style="text-align: center; padding: 60px;">
                <i class="fas fa-arrow-up" style="font-size: 64px; color: var(--text-light); margin-bottom: 16px;"></i>
                <h3 style="color: var(--text-light);">Selecciona un hijo para ver sus restricciones</h3>
            </div>
        `;
        return;
    }
    
    try {
        showLoading();
        currentHijoId = parseInt(hijoId);
        btnAdd.disabled = false;
        
        restricciones = await API.getRestrictions(currentHijoId);
        renderRestrictions();
        closeLoading();
    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudieron cargar las restricciones', 'error');
    }
}

function renderRestrictions() {
    const container = document.getElementById('restrictionsContainer');
    
    if (restricciones.length === 0) {
        container.innerHTML = `
            <div class="card" style="text-align: center; padding: 60px;">
                <i class="fas fa-check-circle" style="font-size: 64px; color: var(--success); margin-bottom: 16px;"></i>
                <h3>Sin restricciones alimentarias</h3>
                <p style="color: var(--text-light); margin-bottom: 24px;">
                    Este hijo no tiene restricciones registradas
                </p>
                <button class="btn btn-primary" onclick="showAddRestrictionModal()">
                    <i class="fas fa-plus"></i> Agregar Primera Restricción
                </button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = `
        <div class="card">
            <h3 style="margin-bottom: 16px;">
                <i class="fas fa-ban" style="color: var(--danger);"></i> 
                Restricciones Activas (${restricciones.length})
            </h3>
            <div class="grid grid-2">
                ${restricciones.map(r => renderRestrictionCard(r)).join('')}
            </div>
        </div>
    `;
}

function renderRestrictionCard(restriccion) {
    const isAlergia = restriccion.tipo === 'alergia';
    const icon = isAlergia ? 'fa-exclamation-triangle' : 'fa-ban';
    const color = isAlergia ? 'var(--danger)' : 'var(--warning)';
    const title = isAlergia ? 'Alergia' : 'Restricción';
    
    let alimentoNombre = '';
    if (isAlergia && restriccion.alimento_id) {
        const alimento = alimentos.find(a => a.id === restriccion.alimento_id);
        alimentoNombre = alimento ? alimento.nombre : `Alimento #${restriccion.alimento_id}`;
    }
    
    const displayText = isAlergia ? alimentoNombre : restriccion.texto;
    
    return `
        <div class="card" style="border-left: 4px solid ${color};">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                        <i class="fas ${icon}" style="color: ${color};"></i>
                        <span class="badge ${isAlergia ? 'badge-danger' : 'badge-warning'}">${title}</span>
                    </div>
                    <h4 style="margin: 0; font-size: 18px;">${displayText}</h4>
                    ${isAlergia ? '<p style="color: var(--text-light); font-size: 12px; margin-top: 4px;">Evitar completamente</p>' : ''}
                </div>
                <button class="btn btn-danger" style="padding: 8px 12px;" onclick="deleteRestriction(${restriccion.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
}

// Modal para agregar restricción
async function showAddRestrictionModal() {
    if (!currentHijoId) {
        showNotification('Error', 'Selecciona un hijo primero', 'warning');
        return;
    }
    
    const { value: tipoRestriction } = await Swal.fire({
        title: 'Tipo de Restricción',
        text: 'Selecciona el tipo de restricción que deseas agregar',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: '<i class="fas fa-exclamation-triangle"></i> Alergia Específica',
        cancelButtonText: '<i class="fas fa-ban"></i> Restricción General',
        confirmButtonColor: '#F44336',
        cancelButtonColor: '#FF9800',
        showCloseButton: true,
        allowOutsideClick: false
    });
    
    if (tipoRestriction === true) {
        // Alergia específica
        await showAlergiaModal();
    } else if (tipoRestriction === false) {
        // Restricción general
        await showProhibidoModal();
    }
}

async function showAlergiaModal() {
    const alimentosOptions = alimentos
        .map(a => `<option value="${a.id}">${a.nombre}</option>`)
        .join('');
    
    const { value: alimentoId } = await Swal.fire({
        title: 'Alergia Específica',
        html: `
            <div style="text-align: left;">
                <label style="display: block; margin-bottom: 8px; font-weight: 600;">
                    Selecciona el alimento al que es alérgico:
                </label>
                <select id="swal-alimento" class="swal2-input" style="width: 100%;">
                    <option value="">-- Selecciona un alimento --</option>
                    ${alimentosOptions}
                </select>
            </div>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: '#F44336',
        cancelButtonColor: '#666',
        confirmButtonText: 'Agregar Alergia',
        preConfirm: () => {
            const value = document.getElementById('swal-alimento').value;
            if (!value) {
                Swal.showValidationMessage('Debes seleccionar un alimento');
            }
            return value;
        }
    });
    
    if (alimentoId) {
        await createRestriction({
            hijo_id: currentHijoId,
            tipo: 'alergia',
            alimento_id: parseInt(alimentoId),
            texto: null
        });
    }
}

async function showProhibidoModal() {
    const { value: texto } = await Swal.fire({
        title: 'Restricción General',
        html: `
            <div style="text-align: left;">
                <label style="display: block; margin-bottom: 8px; font-weight: 600;">
                    Describe la restricción:
                </label>
                <input id="swal-texto" class="swal2-input" placeholder="Ej: Sin azúcares refinados" style="width: 100%;">
                <p style="font-size: 12px; color: var(--text-light); margin-top: 8px;">
                    Esta restricción se aplicará de forma general
                </p>
            </div>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: '#FF9800',
        cancelButtonColor: '#666',
        confirmButtonText: 'Agregar Restricción',
        preConfirm: () => {
            const value = document.getElementById('swal-texto').value;
            if (!value || !value.trim()) {
                Swal.showValidationMessage('Debes ingresar una descripción');
            }
            return value;
        }
    });
    
    if (texto) {
        await createRestriction({
            hijo_id: currentHijoId,
            tipo: 'prohibido',
            alimento_id: null,
            texto: texto.trim()
        });
    }
}

async function createRestriction(data) {
    try {
        showLoading();
        await API.createRestriction(data);
        closeLoading();
        showNotification('Éxito', 'Restricción agregada correctamente', 'success');
        loadRestrictions();
    } catch (error) {
        closeLoading();
        showNotification('Error', error.message || 'No se pudo agregar la restricción', 'error');
    }
}

async function deleteRestriction(id) {
    const result = await confirmAction(
        '¿Eliminar restricción?',
        'Esta acción no se puede deshacer'
    );
    
    if (result.isConfirmed) {
        try {
            showLoading();
            await API.deleteRestriction(id);
            closeLoading();
            showNotification('Éxito', 'Restricción eliminada correctamente', 'success');
            loadRestrictions();
        } catch (error) {
            closeLoading();
            showNotification('Error', error.message || 'No se pudo eliminar la restricción', 'error');
        }
    }
}

// Inicializar
loadInitialData();