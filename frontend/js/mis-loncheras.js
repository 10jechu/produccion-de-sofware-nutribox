requireAuth();
        
let lunchboxes = [];
let hijos = []; 
        
function getBadgeClass(estado) {
    if (estado === "Confirmada") return "bg-success";
    if (estado === "Borrador") return "bg-warning text-dark";
    return "bg-secondary";
}

function formatCurrency(value) {
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(value);
}

function getHijoName(hijoId) {
    const hijo = hijos.find(h => h.id === hijoId);
    return hijo ? hijo.nombre : `Hijo #${hijoId}`; 
}

async function loadLunchboxes() {
    try {
        showLoading();
        
        const user = getUser();
        // Cargar hijos y loncheras base
        const baseLunchboxes = await API.getLunchboxes();
        hijos = await API.getChildren(user.id);
        
        // Obtener el detalle completo (nombre del hijo, items, calorías, costo) para cada lonchera
        const detailedLunchboxesPromises = baseLunchboxes.map(lb => 
            API.getLunchboxDetail(lb.id)
        );
        
        const detailedLunchboxes = await Promise.all(detailedLunchboxesPromises);

        // Combinar el detalle con los datos y prepararlos para la tabla
        lunchboxes = detailedLunchboxes.map(detail => ({
            ...detail,
            hijo_nombre: getHijoName(detail.hijo.id), 
            items_count: detail.items.length,
            total_calorias: detail.nutricion_total.calorias.toFixed(0), 
            total_costo: detail.nutricion_total.costo_total // El costo ya viene calculado
        }));
        
        renderLunchboxes();
        closeLoading();
    } catch (error) {
        closeLoading();
        if (error.message.includes("Token inválido")) {
            logout();
            return;
        }
        showNotification("Error", "No se pudieron cargar los detalles de las loncheras.", "error");
    }
}

function renderLunchboxes() {
    const tbody = document.getElementById("lunchboxesTableBody");

    if (lunchboxes.length === 0) {
        tbody.innerHTML = "<tr><td colspan=\"7\" class=\"text-center text-muted\">No hay loncheras registradas</td></tr>";
        return;
    }

    tbody.innerHTML = lunchboxes.map(lb => `
        <tr>
            <td>${formatDate(lb.fecha)}</td>
            <td><strong>${lb.hijo_nombre}</strong></td>
            <td>
                <span class="badge ${getBadgeClass(lb.estado)}">
                    ${lb.estado}
                </span>
            </td>
            <td>${lb.items_count} items</td>
            <td>${lb.total_calorias} kcal</td>
            <td>${formatCurrency(lb.total_costo)}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary me-1" onclick="viewDetail(${lb.id})">
                    <i class="fas fa-eye"></i>
                    <span class="d-none d-md-inline"> Ver Detalle</span>
                </button>

                <button class="btn btn-sm btn-outline-danger" onclick="deleteLunchbox(${lb.id})">
                    <i class="fas fa-trash"></i>
                </button>

            </td>
        </tr>
    `).join("");
}

async function viewDetail(id) {
    try {
        // Obtenemos el detalle ya cargado para evitar una llamada adicional
        const detail = lunchboxes.find(lb => lb.id === id); 
        if (!detail) throw new Error("Detalle de lonchera no encontrado.");

        // Formateo del contenido del modal
        const itemsList = detail.items.map(item => 
            `<li class="list-group-item d-flex justify-content-between align-items-center">
                <span>${item.nombre}</span> 
                <span class="badge bg-light text-dark">${item.cantidad}x - ${item.kcal.toFixed(0)} kcal / ${formatCurrency(item.costo)}</span> 
             </li>`
        ).join("");
        
        const alertas = detail.alertas.map(a => 
            `<div class="alert ${a.includes("ALERTA") ? "alert-danger" : "alert-warning"} p-2 mt-2 mb-0" role="alert">
                <i class="fas fa-exclamation-triangle me-1"></i> ${a} 
            </div>`
        ).join("");

        Swal.fire({
            title: `Lonchera para ${detail.hijo_nombre}`,
            html: `
                ${alertas}
                <div class="text-start mt-3">
                    <h5 class="mb-3 border-bottom pb-2">Información General</h5>
                    <div class="row">
                        <div class="col-6 mb-2"><strong>Fecha:</strong> ${formatDate(detail.fecha)}</div>
                        <div class="col-6 mb-2"><strong>Estado:</strong> <span class="badge ${getBadgeClass(detail.estado)}">${detail.estado}</span></div>
                        <div class="col-12 mb-2"><strong>Entrega:</strong> ${detail.direccion ? detail.direccion.etiqueta + " - " + detail.direccion.direccion : "Sin dirección de envío"}</div>
                    </div>
                    
                    <h5 class="mt-4 mb-2 border-bottom pb-2">Alimentos (${detail.items.length})</h5>
                    <ul class="list-group list-group-flush">${itemsList}</ul>
                    
                    <h5 class="mt-4 mb-2 border-bottom pb-2">Nutrición y Costo</h5>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item d-flex justify-content-between px-0">Calorías: <strong class="text-danger">${detail.nutricion_total.calorias.toFixed(1)} kcal</strong></li>
                        <li class="list-group-item d-flex justify-content-between px-0">Proteínas: <strong>${detail.nutricion_total.proteinas.toFixed(1)} g</strong></li>
                        <li class="list-group-item d-flex justify-content-between px-0">Carbohidratos: <strong>${detail.nutricion_total.carbohidratos.toFixed(1)} g</strong></li>
                        <li class="list-group-item d-flex justify-content-between px-0">Costo Total: <strong>${formatCurrency(detail.nutricion_total.costo_total)}</strong></li>
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

    async function deleteLunchbox(id) {
    const result = await confirmAction(
        "¿Eliminar Lonchera?",
        "Esta acción eliminará la lonchera y todos sus alimentos asociados de forma permanente." // Puedes cambiar este texto si el backend hace soft delete
    );

    if (result.isConfirmed) {
        try {
            showLoading();
            // Asegúrate de que API.deleteLunchbox exista en api.js
            await API.deleteLunchbox(id);
            closeLoading();
            showNotification("Éxito", "Lonchera eliminada correctamente", "success");
            loadLunchboxes(); // Recargar la lista
        } catch (error) {
            closeLoading();
            showNotification("Error", error.message, "error");
        }
    }
}

loadLunchboxes();