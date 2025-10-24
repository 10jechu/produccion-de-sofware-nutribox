requireAuth();

let direcciones = [];

async function loadAddresses() {
    try {
        showLoading();
        const user = getUser();
        direcciones = await API.getAddresses(user.id);
        renderAddresses();
        closeLoading();
    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudieron cargar las direcciones', 'error');
    }
}

function renderAddresses() {
    const container = document.getElementById('addressesContainer');
    
    if (direcciones.length === 0) {
        container.innerHTML = `
            <div class="card" style="grid-column: 1 / -1; text-align: center; padding: 60px;">
                <i class="fas fa-map-marker-alt" style="font-size: 64px; color: var(--primary); margin-bottom: 16px;"></i>
                <h3>No tienes direcciones registradas</h3>
                <p style="color: var(--text-light); margin-bottom: 24px;">Agrega una dirección de entrega</p>
                <button class="btn btn-primary" onclick="showAddAddressModal()">
                    <i class="fas fa-plus"></i> Agregar Dirección
                </button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = direcciones.map(dir => `
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;">
                <div style="flex: 1;">
                    <h4 style="margin-bottom: 4px;">${dir.etiqueta}</h4>
                    <p style="color: var(--text-light); margin-bottom: 4px;">${dir.direccion}</p>
                    <p style="color: var(--text-light); font-size: 14px;">${dir.barrio}, ${dir.ciudad}</p>
                </div>
                <button class="btn btn-danger" style="padding: 8px 12px;" onclick="deleteAddress(${dir.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

async function showAddAddressModal() {
    const { value: formValues } = await Swal.fire({
        title: 'Agregar Dirección',
        html: `
            <input id="swal-etiqueta" class="swal2-input" placeholder="Etiqueta (Ej: Casa)">
            <input id="swal-direccion" class="swal2-input" placeholder="Dirección completa">
            <input id="swal-barrio" class="swal2-input" placeholder="Barrio">
            <input id="swal-ciudad" class="swal2-input" placeholder="Ciudad">
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: '#4CAF50',
        cancelButtonColor: '#F44336',
        preConfirm: () => {
            return {
                etiqueta: document.getElementById('swal-etiqueta').value,
                direccion: document.getElementById('swal-direccion').value,
                barrio: document.getElementById('swal-barrio').value,
                ciudad: document.getElementById('swal-ciudad').value
            };
        }
    });
    
    if (formValues) {
        const { etiqueta, direccion, barrio, ciudad } = formValues;
        
        if (!etiqueta || !direccion || !barrio || !ciudad) {
            showNotification('Error', 'Todos los campos son obligatorios', 'warning');
            return;
        }
        
        try {
            showLoading();
            const user = getUser();
            await API.createAddress({
                usuario_id: user.id,
                etiqueta,
                direccion,
                barrio,
                ciudad
            });
            closeLoading();
            showNotification('Éxito', 'Dirección agregada correctamente', 'success');
            loadAddresses();
        } catch (error) {
            closeLoading();
            showNotification('Error', error.message, 'error');
        }
    }
}

async function deleteAddress(id) {
    const result = await confirmAction(
        '¿Eliminar dirección?',
        'Esta acción no se puede deshacer'
    );
    
    if (result.isConfirmed) {
        try {
            showLoading();
            await API.deleteAddress(id);
            closeLoading();
            showNotification('Éxito', 'Dirección eliminada correctamente', 'success');
            loadAddresses();
        } catch (error) {
            closeLoading();
            showNotification('Error', error.message, 'error');
        }
    }
}

loadAddresses();
