requireAuth();

let hijos = [];

async function loadHijos() {
    try {
        showLoading();
        const user = getUser();
        // Carga los hijos del usuario
        hijos = await API.getChildren(user.id);
        renderHijos();
        closeLoading();
    } catch (error) {
        closeLoading();
        // Si hay error en el token, forzamos el logout.
        if (error.message.includes("Token inválido")) {
            logout();
            return;
        }
        showNotification("Error", "No se pudieron cargar los hijos", "error");
    }
}

function renderHijos() {
    const container = document.getElementById("hijosContainer");
    
    if (hijos.length === 0) {
        container.innerHTML = `
            <div class="col-12">
                <div class="card p-5 text-center card-shadow">
                    <i class="fas fa-child text-primary-nb mb-3" style="font-size: 48px;"></i>
                    <h3 class="h4">No tienes hijos registrados</h3>
                    <p class="text-muted mb-4">Comienza agregando tu primer hijo</p>
                    <button class="btn btn-primary-nb w-auto mx-auto" onclick="showAddChildModal()">
                        <i class="fas fa-plus me-1"></i> Agregar Hijo
                    </button>
                </div>
            </div>
        `;
        return;
    }
    
    container.innerHTML = hijos.map(hijo => `
        <div class="col-lg-4 col-md-6">
            <div class="card p-4 card-shadow h-100">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <h5 class="fw-bold mb-0">${hijo.nombre}</h5>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteHijo(${hijo.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                <div class="border-top pt-3 mt-auto">
                    <button class="btn btn-sm btn-outline-primary w-100 mb-2" onclick="viewHijoDetail(${hijo.id})">
                        <i class="fas fa-eye me-1"></i> Ver Detalle
                    </button>
                    <a href="crear-lonchera.html?hijoId=${hijo.id}" class="btn btn-sm btn-primary-nb w-100">
                        <i class="fas fa-plus me-1"></i> Crear Lonchera
                    </a>
                </div>
            </div>
        </div>
    `).join("");
}

async function showAddChildModal() {
    const { value: nombre } = await Swal.fire({
        title: "Agregar Hijo",
        input: "text",
        inputLabel: "Nombre del hijo",
        inputPlaceholder: "Ej: Juan Pérez",
        showCancelButton: true,
        confirmButtonColor: "#4CAF50",
        cancelButtonColor: "#DC3545",
        confirmButtonText: "Agregar",
        cancelButtonText: "Cancelar",
        inputValidator: (value) => {
            if (!value) {
                return "Debes ingresar un nombre";
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
            showNotification("Éxito", "Hijo agregado correctamente", "success");
            loadHijos();
        } catch (error) {
            closeLoading();
            showNotification("Error", error.message, "error");
        }
    }
}

async function deleteHijo(id) {
    const result = await confirmAction(
        "¿Eliminar hijo?",
        "Esta acción eliminará al hijo y todas sus loncheras asociadas."
    );
    
    if (result.isConfirmed) {
        try {
            showLoading();
            await API.deleteChild(id);
            closeLoading();
            showNotification("Éxito", "Hijo eliminado correctamente", "success");
            loadHijos();
        } catch (error) {
            closeLoading();
            showNotification("Error", error.message, "error");
        }
    }
}

async function viewHijoDetail(id) {
    try {
        showLoading();
        // Usar la API de detalle para obtener estadísticas y restricciones
        const detail = await API.getChildDetail(id);
        closeLoading();
        
        const restriccionesList = detail.restricciones.length > 0
            ? detail.restricciones.map(r => 
                `<li class="list-group-item d-flex justify-content-between align-items-start py-1 px-0">${r.tipo.toUpperCase()}: ${r.alimento_nombre || r.texto}</li>`
              ).join("")
            : '<li class="list-group-item text-muted px-0">Sin restricciones registradas.</li>';
        
        Swal.fire({
            title: detail.nombre,
            html: `
                <div class="text-start">
                    <p class="text-muted">ID: ${detail.id}</p>
                    
                    <h5 class="mt-3">Restricciones: <a href="restricciones.html?hijoId=${detail.id}" class="small badge bg-primary-nb text-white text-decoration-none">Gestionar Restricciones</a></h5>
                    <ul class="list-group list-group-flush border-top border-bottom">${restriccionesList}</ul>
                    
                    <h5 class="mt-4">Estadísticas:</h5>
                    <ul class="list-unstyled mb-0">
                        <li><strong>Total de Loncheras:</strong> ${detail.estadisticas.total_loncheras}</li>
                        <li><strong>Promedio de Calorías:</strong> <span class="badge bg-success">${detail.estadisticas.promedio_calorias} kcal</span></li>
                    </ul>
                </div>
            `,
            width: 600,
            confirmButtonColor: "#4CAF50"
        });
    } catch (error) {
        closeLoading();
        showNotification("Error", "No se pudo cargar el detalle", "error");
    }
}

loadHijos();