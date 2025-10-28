requireAuth();

let hijos = [];
let foods = [];
let currentRestrictions = [];

async function loadInitialData() {
    try {
        showLoading();
        const user = getUser();
        // Carga de hijos y alimentos en paralelo
        [hijos, foods] = await Promise.all([
            API.getChildren(user.id),
            API.getFoods("all")
        ]);
        
        populateHijoSelect();
        closeLoading();
    } catch (error) {
        closeLoading();
        if (error.message.includes("Token inválido")) {
            logout();
            return;
        }
        showNotification("Error", "No se pudieron cargar los hijos o alimentos", "error");
    }
}

function populateHijoSelect() {
    const hijoSelect = document.getElementById("hijoSelect");
    hijoSelect.innerHTML = "<option value=\"\">Selecciona un hijo</option>" +
        hijos.map(h => `<option value="${h.id}">${h.nombre}</option>`).join("");
    
    // Intenta cargar si hay un hijo preseleccionado (ej. desde el detalle de hijos)
    const urlParams = new URLSearchParams(window.location.search);
    const preselectedHijoId = urlParams.get("hijoId");
    if (preselectedHijoId) {
        hijoSelect.value = preselectedHijoId;
        loadRestrictions();
    }
}

async function loadRestrictions() {
    const hijoId = document.getElementById("hijoSelect").value;
    const addButton = document.getElementById("addRestrictionBtn");

    if (!hijoId) {
        document.getElementById("restrictionsContainer").innerHTML = '<p class="text-center text-muted">Selecciona un hijo para ver sus restricciones.</p>';
        addButton.disabled = true;
        return;
    }
    
    try {
        showLoading();
        currentRestrictions = await API.getRestrictions(hijoId);
        renderRestrictions();
        addButton.disabled = false;
        closeLoading();
    } catch (error) {
        closeLoading();
        document.getElementById("restrictionsContainer").innerHTML = '<p class="text-center text-danger">Error al cargar restricciones: ' + error.message + '</p>';
        addButton.disabled = true;
    }
}

function renderRestrictions() {
    const container = document.getElementById("restrictionsContainer");
    
    if (currentRestrictions.length === 0) {
        container.innerHTML = '<p class="text-center text-muted py-4">Este hijo no tiene restricciones registradas. ¡Agrega la primera!</p>';
        return;
    }
    
    container.innerHTML = `<ul class="list-group list-group-flush">${currentRestrictions.map(r => 
        `<li class="list-group-item d-flex justify-content-between align-items-center">
            <div>
                <span class="badge ${r.tipo === "alergia" ? "bg-danger" : "bg-warning text-dark"} me-2">${r.tipo.toUpperCase()}</span>
                ${r.tipo === "alergia" ? `Alergia a: <strong>${foods.find(f => f.id === r.alimento_id)?.nombre || "Alimento desconocido"}</strong>` : `Prohibido (contiene): <strong>${r.texto}</strong>`}
            </div>
            <button class="btn btn-sm btn-outline-danger" onclick="deleteRestriction(${r.id})">
                <i class="fas fa-trash"></i>
            </button>
        </li>`
    ).join("")}</ul>`;
}

async function showAddRestrictionModal() {
    const hijoId = document.getElementById("hijoSelect").value;
    if (!hijoId) return;

    const foodOptions = foods.filter(f => f.activo).map(f => 
        `<option value="${f.id}">${f.nombre}</option>`
    ).join("");

    const { value: formValues } = await Swal.fire({
        title: "Agregar Restricción",
        html: `
            <select id="swal-tipo" class="form-select mb-3">
                <option value="alergia">Alergia (a un alimento específico)</option>
                <option value="prohibido">Prohibido (match por texto)</option>
            </select>
            <div id="alimento-field" class="mb-3">
                <select id="swal-alimento" class="form-select">
                    <option value="">Selecciona Alimento</option>
                    ${foodOptions}
                </select>
            </div>
            <div id="texto-field" class="mb-3" style="display: none;">
                <input id="swal-texto" class="form-control" placeholder="Ej: maní, gluten, colorante rojo">
            </div>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: "#4CAF50",
        cancelButtonColor: "#DC3545",
        confirmButtonText: "Guardar Restricción",
        preConfirm: () => {
            const tipo = document.getElementById("swal-tipo").value;
            const alimentoId = document.getElementById("swal-alimento").value;
            const texto = document.getElementById("swal-texto").value;
            
            if (tipo === "alergia" && !alimentoId) {
                Swal.showValidationMessage(`Debes seleccionar un alimento para la alergia`);
                return false;
            }
            if (tipo === "prohibido" && !texto.trim()) {
                Swal.showValidationMessage(`El campo de texto es requerido para esta restricción`);
                return false;
            }
            
            return {
                hijo_id: parseInt(hijoId),
                tipo,
                alimento_id: tipo === "alergia" ? parseInt(alimentoId) : null,
                texto: tipo === "prohibido" ? texto.trim() : null
            };
        },
        didOpen: () => {
            const tipoSelect = document.getElementById("swal-tipo");
            const alimentoField = document.getElementById("alimento-field");
            const textoField = document.getElementById("texto-field");

            const toggleFields = () => {
                if (tipoSelect.value === "alergia") {
                    alimentoField.style.display = "block";
                    textoField.style.display = "none";
                } else {
                    alimentoField.style.display = "none";
                    textoField.style.display = "block";
                }
            };
            tipoSelect.addEventListener("change", toggleFields);
            toggleFields();
        }
    });
    
    if (formValues) {
        try {
            showLoading();
            await API.createRestriction(formValues);
            closeLoading();
            showNotification("Éxito", "Restricción agregada correctamente", "success");
            loadRestrictions();
        } catch (error) {
            closeLoading();
            showNotification("Error", error.message, "error");
        }
    }
}

async function deleteRestriction(id) {
    const result = await confirmAction(
        "¿Eliminar restricción?",
        "Esta restricción será eliminada permanentemente del perfil del hijo."
    );
    
    if (result.isConfirmed) {
        try {
            showLoading();
            await API.deleteRestriction(id);
            closeLoading();
            showNotification("Éxito", "Restricción eliminada", "success");
            loadRestrictions();
        } catch (error) {
            closeLoading();
            showNotification("Error", error.message, "error");
        }
    }
}

loadInitialData();