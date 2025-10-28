requireAuth();

let hijos = [];
let alimentos = [];

async function loadHijos() {
    try {
        showLoading();
        const user = getUser();
        hijos = await API.getChildren(user.id);
        alimentos = await API.getFoods('true');
        renderHijos();
        closeLoading();
    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudieron cargar los hijos', 'error');
    }
}

function renderHijos() {
    const container = document.getElementById('hijosContainer');

    if (hijos.length === 0) {
        container.innerHTML = `
            <div class="card" style="grid-column: 1 / -1; text-align: center; padding: 60px;">
                <i class="fas fa-child" style="font-size: 64px; color: var(--primary); margin-bottom: 16px;"></i>
                <h3>No tienes hijos registrados</h3>
                <p style="color: var(--text-light); margin-bottom: 24px;">Comienza agregando tu primer hijo</p>
                <button class="btn btn-primary" onclick="showAddChildModal()">
                    <i class="fas fa-plus"></i> Agregar Hijo
                </button>
            </div>
        `;
        return;
    }

    container.innerHTML = hijos.map(hijo => `
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;">
                <div style="flex: 1;">
                    <h3 style="margin-bottom: 8px;">${hijo.nombre}</h3>
                    <p style="color: var(--text-light); font-size: 14px;">ID: ${hijo.id}</p>
                </div>
                <button class="btn btn-danger" style="padding: 8px 12px;" onclick="deleteHijo(${hijo.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
            <div style="border-top: 1px solid var(--border); padding-top: 16px;">
                <button class="btn btn-outline" style="width: 100%; margin-bottom: 8px;" onclick="viewHijoDetail(${hijo.id})">
                    <i class="fas fa-eye"></i> Ver Detalle
                </button>
                <button class="btn btn-secondary" style="width: 100%; margin-bottom: 8px;" onclick="manageRestrictions(${hijo.id}, '${hijo.nombre}')">
                    <i class="fas fa-shield-alt"></i> Restricciones
                </button>
                <a href="crear-lonchera.html" class="btn btn-primary" style="width: 100%; text-align: center;">
                    <i class="fas fa-plus"></i> Crear Lonchera
                </a>
            </div>
        </div>
    `).join('');
}

async function showAddChildModal() {
    const { value: nombre } = await Swal.fire({
        title: 'Agregar Hijo',
        input: 'text',
        inputLabel: 'Nombre del hijo',
        inputPlaceholder: 'Ej: Juan Pérez',
        showCancelButton: true,
        confirmButtonColor: '#4CAF50',
        cancelButtonColor: '#F44336',
        confirmButtonText: 'Agregar',
        cancelButtonText: 'Cancelar',
        inputValidator: (value) => {
            if (!value) {
                return 'Debes ingresar un nombre';
            }
        }
    });

    if (nombre) {
        try {
            showLoading();
            const user = getUser();
            await API.createChild({
                nombre,
                usuario_id: user.id
            });
            closeLoading();
            showNotification('Éxito', 'Hijo agregado correctamente', 'success');
            loadHijos();
        } catch (error) {
            closeLoading();
            showNotification('Error', error.message, 'error');
        }
    }
}

async function deleteHijo(id) {
    const result = await confirmAction(
        '¿Eliminar hijo?',
        'Esta acción no se puede deshacer'
    );

    if (result.isConfirmed) {
        try {
            showLoading();
            await API.deleteChild(id);
            closeLoading();
            showNotification('Éxito', 'Hijo eliminado correctamente', 'success');
            loadHijos();
        } catch (error) {
            closeLoading();
            showNotification('Error', error.message, 'error');
        }
    }
}

async function viewHijoDetail(id) {
    try {
        showLoading();
        const detail = await API.getChildDetail(id);
        closeLoading();

        const restriccionesList = detail.restricciones.length > 0
            ? detail.restricciones.map(r =>
                `<li>${r.tipo === 'alergia' ? '🔴 Alergia' : '⚠️ Prohibido'}: ${r.alimento_nombre || r.texto}</li>`
              ).join('')
            : '<li>Sin restricciones</li>';

        Swal.fire({
            title: detail.nombre,
            html: `
                <div style="text-align: left;">
                    <h4>Padre:</h4>
                    <p>${detail.padre.nombre}</p>
                    
                    <h4>Restricciones Alimentarias:</h4>
                    <ul>${restriccionesList}</ul>
                    
                    <h4>Estadísticas:</h4>
                    <p>Total de loncheras: ${detail.estadisticas.total_loncheras}</p>
                    <p>Promedio de calorías: ${detail.estadisticas.promedio_calorias} kcal</p>
                </div>
            `,
            width: 600,
            confirmButtonColor: '#4CAF50'
        });
    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudo cargar el detalle', 'error');
    }
}

async function manageRestrictions(hijoId, hijoNombre) {
    try {
        showLoading();
        const restricciones = await API.getRestrictions(hijoId);
        closeLoading();

        const restriccionesList = restricciones.length > 0
            ? restricciones.map(r => {
                const icon = r.tipo === 'alergia' ? '🔴' : '⚠️';
                const label = r.tipo === 'alergia' ? 'Alergia' : 'Prohibido';
                const name = r.alimento_nombre || r.texto;
                return `
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; border-bottom: 1px solid #eee;">
                        <span>${icon} <strong>${label}:</strong> ${name}</span>
                        <button onclick="deleteRestriction(${r.id}, ${hijoId}, '${hijoNombre}')" style="background: #f44336; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer;">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                `;
              }).join('')
            : '<p style="text-align: center; color: #666; padding: 20px;">No hay restricciones registradas</p>';

        Swal.fire({
            title: `Restricciones de ${hijoNombre}`,
            html: `
                <div style="text-align: left; max-height: 400px; overflow-y: auto;">
                    ${restriccionesList}
                </div>
                <div style="margin-top: 20px; display: flex; gap: 10px;">
                    <button onclick="addAlergiaModal(${hijoId}, '${hijoNombre}')" class="btn btn-danger" style="flex: 1;">
                        🔴 Agregar Alergia
                    </button>
                    <button onclick="addProhibidoModal(${hijoId}, '${hijoNombre}')" class="btn btn-warning" style="flex: 1;">
                        ⚠️ Agregar Prohibido
                    </button>
                </div>
            `,
            width: 600,
            showConfirmButton: false,
            showCloseButton: true
        });
    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudieron cargar las restricciones', 'error');
    }
}

async function addAlergiaModal(hijoId, hijoNombre) {
    const alimentosOptions = alimentos.map(a =>
        `<option value="${a.id}">${a.nombre}</option>`
    ).join('');

    const { value: alimentoId } = await Swal.fire({
        title: `Agregar Alergia para ${hijoNombre}`,
        html: `
            <select id="swal-alimento" class="swal2-input" style="width: 80%;">
                <option value="">Selecciona un alimento</option>
                ${alimentosOptions}
            </select>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: '#f44336',
        cancelButtonColor: '#666',
        confirmButtonText: 'Agregar',
        preConfirm: () => {
            return document.getElementById('swal-alimento').value;
        }
    });

    if (alimentoId) {
        try {
            showLoading();
            await API.createRestriction({
                hijo_id: hijoId,
                tipo: 'alergia',
                alimento_id: parseInt(alimentoId),
                texto: null
            });
            closeLoading();
            showNotification('Éxito', 'Alergia agregada correctamente', 'success');
            manageRestrictions(hijoId, hijoNombre);
        } catch (error) {
            closeLoading();
            showNotification('Error', error.message, 'error');
        }
    }
}

async function addProhibidoModal(hijoId, hijoNombre) {
    const { value: texto } = await Swal.fire({
        title: `Agregar Restricción para ${hijoNombre}`,
        input: 'text',
        inputLabel: 'Alimento o ingrediente prohibido',
        inputPlaceholder: 'Ej: Nueces, Mariscos, Lácteos',
        showCancelButton: true,
        confirmButtonColor: '#FF9800',
        cancelButtonColor: '#666',
        confirmButtonText: 'Agregar',
        inputValidator: (value) => {
            if (!value) {
                return 'Debes ingresar un texto';
            }
        }
    });

    if (texto) {
        try {
            showLoading();
            await API.createRestriction({
                hijo_id: hijoId,
                tipo: 'prohibido',
                alimento_id: null,
                texto: texto
            });
            closeLoading();
            showNotification('Éxito', 'Restricción agregada correctamente', 'success');
            manageRestrictions(hijoId, hijoNombre);
        } catch (error) {
            closeLoading();
            showNotification('Error', error.message, 'error');
        }
    }
}

async function deleteRestriction(restriccionId, hijoId, hijoNombre) {
    try {
        showLoading();
        await API.deleteRestriction(restriccionId);
        closeLoading();
        showNotification('Éxito', 'Restricción eliminada', 'success');
        manageRestrictions(hijoId, hijoNombre);
    } catch (error) {
        closeLoading();
        showNotification('Error', error.message, 'error');
    }
}

loadHijos();