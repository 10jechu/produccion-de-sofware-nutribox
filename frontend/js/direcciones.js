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
        if (error.message.includes("Token inválido")) {
            logout();
            return;
        }
        showNotification("Error", "No se pudieron cargar las direcciones. Intenta iniciar sesión nuevamente.", "error");
    }
}

function renderAddresses() {
    const container = document.getElementById("addressesContainer");
    
    if (direcciones.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="card p-5 text-center card-shadow">
                    <i class="fas fa-map-marker-alt text-primary-nb mb-3" style="font-size: 48px;"></i>
                    <h4 class="h5">No tienes direcciones registradas</h4>
                    <p class="text-muted mb-4">Agrega una dirección de entrega</p>
                    <button class="btn btn-primary-nb w-auto mx-auto" onclick="showAddAddressModal()">
                        <i class="fas fa-plus me-1"></i> Agregar Dirección
                    </button>
                </div>
            </div>
        `;
        return;
    }
    
    container.innerHTML = direcciones.map(dir => `
        <div class="col-lg-6 col-md-12">
            <div class="card p-3 card-shadow h-100">
                <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                        <h5 class="fw-bold mb-1">${dir.etiqueta}</h5>
                        <p class="text-muted mb-1">${dir.direccion}</p>
                        <p class="small text-dark mb-0">${dir.barrio}, <strong>${dir.ciudad}</strong></p>
                    </div>
                    <button class="btn btn-sm btn-outline-danger ms-3" onclick="deleteAddress(${dir.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join("");
}

async function showAddAddressModal() {
    const { value: formValues } = await Swal.fire({
        title: "Agregar Dirección",
        html: `
            <input id="swal-etiqueta" class="swal2-input form-control" placeholder="Etiqueta (Ej: Casa)" required>
            <input id="swal-direccion" class="swal2-input form-control" placeholder="Dirección completa" required>
            <input id="swal-barrio" class="swal2-input form-control" placeholder="Barrio" required>
            <input id="swal-ciudad" class="swal2-input form-control" placeholder="Ciudad" value="Bogotá" required>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: "#4CAF50",
        cancelButtonColor: "#DC3545",
        confirmButtonText: "Guardar",
        preConfirm: () => {
            const etiqueta = document.getElementById("swal-etiqueta").value;
            const direccion = document.getElementById("swal-direccion").value;
            const barrio = document.getElementById("swal-barrio").value;
            const ciudad = document.getElementById("swal-ciudad").value;

            if (!etiqueta || !direccion) {
                Swal.showValidationMessage("Etiqueta y dirección son requeridas.");
                return false;
            }
            return { etiqueta, direccion, barrio, ciudad };
        }
    });
    
    if (formValues) {
        try {
            showLoading();
            const user = getUser();
            await API.createAddress({
                usuario_id: user.id,
                ...formValues
            });
            closeLoading();
            showNotification("Éxito", "Dirección agregada correctamente", "success");
            loadAddresses();
        } catch (error) {
            closeLoading();
            // Esto captura el error de límite de membresía del backend (RF5.3)
            showNotification("Error", error.message, "error");
        }
    }
}

async function deleteAddress(id) {
    const result = await confirmAction(
        "¿Eliminar dirección?",
        "Esta acción no se puede deshacer"
    );
    
    if (result.isConfirmed) {
        try {
            showLoading();
            await API.deleteAddress(id);
            closeLoading();
            showNotification("Éxito", "Dirección eliminada correctamente", "success");
            loadAddresses();
        } catch (error) {
            closeLoading();
            showNotification("Error", error.message, "error");
        }
    }
}

loadAddresses();