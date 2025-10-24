requireAuth();

let hijos = [];

async function loadHijos() {
    try {
        showLoading();
        const user = getUser();
        hijos = await API.getChildren(user.id);
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
            <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 16px;">
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
                `<li>${r.tipo}: ${r.alimento_nombre || r.texto}</li>`
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

loadHijos();
