requireAuth();

let foods = [];

async function loadFoods() {
    try {
        showLoading();
        // Carga solo alimentos activos (solo consulta para el usuario final)
        foods = await API.getFoods("true"); 
        renderFoods();
        closeLoading();
    } catch (error) {
        closeLoading();
        if (error.message.includes("Token inválido")) {
            logout();
            return;
        }
        showNotification("Error", "No se pudieron cargar los alimentos", "error");
    }
}

function formatCurrency(value) {
    // Formato de moneda COP (ej: $ 1,500)
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(value);
}

function renderFoods() {
    const tbody = document.getElementById("foodsTableBody");

    if (foods.length === 0) {
        tbody.innerHTML = "<tr><td colspan=\"6\" class=\"text-center text-muted\">No hay alimentos registrados.</td></tr>";
        return;
    }

    tbody.innerHTML = foods.map(food => `
        <tr>
            <td>${food.nombre}</td>
            <td>${food.kcal} kcal</td>
            <td>${food.proteinas} g</td>
            <td>${food.carbos} g</td>
            <td>${formatCurrency(food.costo)}</td>
            <td>
                <button class="btn btn-sm btn-outline-info me-1" onclick="viewFoodDetail(${food.id})">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-warning me-1" onclick="showEditFoodModal(${food.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteFood(${food.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join("");
}

async function viewFoodDetail(id) {
    try {
        showLoading();
        const food = foods.find(f => f.id === id);
        closeLoading();
        
        Swal.fire({
            title: food.nombre,
            html: `
                <div class="text-start">
                    <p><strong>Calorías:</strong> ${food.kcal} kcal</p>
                    <p><strong>Proteínas:</strong> ${food.proteinas} g</p>
                    <p><strong>Carbohidratos:</strong> ${food.carbos} g</p>
                    <p><strong>Costo por Unidad:</strong> ${formatCurrency(food.costo)}</p>
                </div>
            `,
            confirmButtonColor: "#4CAF50"
        });
    } catch (error) {
        closeLoading();
        showNotification("Error", "No se pudo cargar el detalle", "error");
    }
}

async function showAddFoodModal() {
    const { value: formValues } = await Swal.fire({
        title: "Agregar Nuevo Alimento",
        html: `
            <input id="swal-nombre" class="swal2-input form-control" placeholder="Nombre del alimento" required>
            <input id="swal-kcal" type="number" step="0.1" class="swal2-input form-control" placeholder="Calorías (kcal)" required>
            <input id="swal-proteinas" type="number" step="0.1" class="swal2-input form-control" placeholder="Proteínas (g)" required>
            <input id="swal-carbos" type="number" step="0.1" class="swal2-input form-control" placeholder="Carbohidratos (g)" required>
            <input id="swal-costo" type="number" step="0.01" class="swal2-input form-control" placeholder="Costo Unitario (COP)" value="0.00" required>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: "#4CAF50",
        cancelButtonColor: "#DC3545",
        confirmButtonText: "Guardar Alimento",
        preConfirm: () => {
            const nombre = document.getElementById("swal-nombre").value;
            const kcal = parseFloat(document.getElementById("swal-kcal").value);
            const proteinas = parseFloat(document.getElementById("swal-proteinas").value);
            const carbos = parseFloat(document.getElementById("swal-carbos").value);
            const costo = parseFloat(document.getElementById("swal-costo").value);

            if (!nombre || isNaN(kcal) || isNaN(proteinas) || isNaN(carbos) || isNaN(costo)) {
                Swal.showValidationMessage("Todos los campos son requeridos y deben ser números válidos.");
                return false;
            }
            if (kcal < 0 || proteinas < 0 || carbos < 0 || costo < 0) {
                 Swal.showValidationMessage("Los valores numéricos no pueden ser negativos.");
                return false;
            }
            return { nombre, kcal, proteinas, carbos, costo };
        }
    });

    if (formValues) {
        try {
            showLoading();
            // Necesitamos crear API.createFood en api.js
            await API.createFood(formValues);
            closeLoading();
            showNotification("Éxito", "Alimento agregado correctamente", "success");
            loadFoods(); // Recargar la lista de alimentos
        } catch (error) {
            closeLoading();
            showNotification("Error", error.message, "error");
        }
    }
}

async function showEditFoodModal(id) {
    const foodToEdit = foods.find(f => f.id === id);
    if (!foodToEdit) {
        showNotification("Error", "No se encontró el alimento para editar.", "error");
        return;
    }

    const { value: formValues } = await Swal.fire({
        title: "Editar Alimento",
        html: `
            <input id="swal-nombre" class="swal2-input form-control" placeholder="Nombre" value="${foodToEdit.nombre}" required>
            <input id="swal-kcal" type="number" step="0.1" class="swal2-input form-control" placeholder="Calorías (kcal)" value="${foodToEdit.kcal}" required>
            <input id="swal-proteinas" type="number" step="0.1" class="swal2-input form-control" placeholder="Proteínas (g)" value="${foodToEdit.proteinas}" required>
            <input id="swal-carbos" type="number" step="0.1" class="swal2-input form-control" placeholder="Carbohidratos (g)" value="${foodToEdit.carbos}" required>
            <input id="swal-costo" type="number" step="0.01" class="swal2-input form-control" placeholder="Costo Unitario (COP)" value="${foodToEdit.costo.toFixed(2)}" required>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonColor: "#4CAF50",
        cancelButtonColor: "#DC3545",
        confirmButtonText: "Guardar Cambios",
        preConfirm: () => {
            const nombre = document.getElementById("swal-nombre").value;
            const kcal = parseFloat(document.getElementById("swal-kcal").value);
            const proteinas = parseFloat(document.getElementById("swal-proteinas").value);
            const carbos = parseFloat(document.getElementById("swal-carbos").value);
            const costo = parseFloat(document.getElementById("swal-costo").value);

            if (!nombre || isNaN(kcal) || isNaN(proteinas) || isNaN(carbos) || isNaN(costo)) {
                Swal.showValidationMessage("Todos los campos son requeridos y deben ser números válidos.");
                return false;
            }
             if (kcal < 0 || proteinas < 0 || carbos < 0 || costo < 0) {
                 Swal.showValidationMessage("Los valores numéricos no pueden ser negativos.");
                return false;
            }
            // Devolvemos solo los campos que podrían cambiar (PATCH)
            return { nombre, kcal, proteinas, carbos, costo };
        }
    });

    if (formValues) {
        try {
            showLoading();
            // Necesitamos crear API.updateFood en api.js
            await API.updateFood(id, formValues);
            closeLoading();
            showNotification("Éxito", "Alimento actualizado correctamente", "success");
            loadFoods(); // Recargar la lista
        } catch (error) {
            closeLoading();
            showNotification("Error", error.message, "error");
        }
    }
}

async function deleteFood(id) {
    const result = await confirmAction(
        "¿Eliminar Alimento?",
        "Esta acción marcará el alimento como inactivo (no se eliminará permanentemente)."
    );

    if (result.isConfirmed) {
        try {
            showLoading();
            // Necesitamos crear API.deleteFood en api.js
            await API.deleteFood(id); // El backend hace soft delete
            closeLoading();
            showNotification("Éxito", "Alimento desactivado correctamente", "success");
            loadFoods(); // Recargar la lista para que desaparezca (si solo muestras activos)
        } catch (error) {
            closeLoading();
            showNotification("Error", error.message, "error");
        }
    }
}

// Llama a loadFoods al final del archivo
loadFoods();
