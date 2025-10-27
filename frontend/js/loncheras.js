requireAuth();

let foods = [];
let selectedFoods = [];
let hijos = [];
let direcciones = [];
let restricciones = []; 

async function loadData() {
    try {
        showLoading();
        const user = getUser();
        
        // Carga de datos en paralelo: Alimentos, Hijos, Direcciones
        [foods, hijos, direcciones] = await Promise.all([
            API.getFoods("true"),
            API.getChildren(user.id),
            API.getAddresses(user.id)
        ]);
        
        populateSelects();
        renderFoods(foods);
        
        // Establecer fecha mínima (hoy)
        const today = new Date().toISOString().split("T")[0];
        document.getElementById("fechaInput").min = today;
        document.getElementById("fechaInput").value = today;
        
        closeLoading();
    } catch (error) {
        closeLoading();
        showNotification("Error", "No se pudieron cargar los datos iniciales. Asegúrate de tener al menos 1 hijo y alimentos registrados.", "error");
    }
}

function formatCurrency(value) {
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(value);
}

function populateSelects() {
    const hijoSelect = document.getElementById("hijoSelect");
    const direccionSelect = document.getElementById("direccionSelect");
    
    hijoSelect.innerHTML = `<option value="">Selecciona un hijo</option>` +
        hijos.map(h => `<option value="${h.id}">${h.nombre}</option>`).join("");
    
    direccionSelect.innerHTML = `<option value="">Selecciona una dirección (opcional)</option>` +
        direcciones.map(d => `<option value="${d.id}">${d.etiqueta} - ${d.direccion}</option>`).join("");

    hijoSelect.addEventListener("change", loadChildRestrictions);
}

async function loadChildRestrictions() {
    const hijoId = document.getElementById("hijoSelect").value;
    if (!hijoId) {
        restricciones = [];
        updateNutrition(); 
        return;
    }
    try {
        // Cargar las restricciones del hijo seleccionado
        restricciones = await API.getRestrictions(hijoId);
        updateNutrition(); // Vuelve a calcular nutrición y alertas
    } catch (error) {
        restricciones = [];
        updateNutrition();
        console.error("Error al cargar restricciones:", error);
    }
}

function renderFoods(foodList) {
    const container = document.getElementById("foodsContainer");
    
    container.innerHTML = foodList.map(food => `
        <div class="d-flex justify-content-between align-items-center p-2 border-bottom">
            <div>
                <strong>${food.nombre}</strong>
                <div class="small text-muted">
                    ${food.kcal} kcal | ${formatCurrency(food.costo)}/u
                </div>
            </div>
            <button class="btn btn-sm bg-primary-nb text-white" onclick="addFood(${food.id})">
                <i class="fas fa-plus"></i>
            </button>
        </div>
    `).join("");
}

function addFood(foodId) {
    const food = foods.find(f => f.id === foodId);
    if (!food) return;
    
    const existing = selectedFoods.find(f => f.id === foodId);
    if (existing) {
        existing.cantidad++;
    } else {
        selectedFoods.push({
            id: food.id,
            nombre: food.nombre,
            kcal: food.kcal,
            proteinas: food.proteinas,
            carbos: food.carbos,
            costo: food.costo, // Usar el costo real del backend
            cantidad: 1
        });
    }
    
    renderSelectedFoods();
    updateNutrition();
}

function removeFood(foodId) {
    selectedFoods = selectedFoods.filter(f => f.id !== foodId);
    renderSelectedFoods();
    updateNutrition();
}

function updateQuantity(foodId, cantidad) {
    const food = selectedFoods.find(f => f.id === foodId);
    if (food) {
        food.cantidad = Math.max(1, parseInt(cantidad));
        renderSelectedFoods();
        updateNutrition();
    }
}

function renderSelectedFoods() {
    const container = document.getElementById("selectedFoodsContainer");
    
    if (selectedFoods.length === 0) {
        container.innerHTML = `<p class="text-center text-muted">No hay alimentos seleccionados</p>`;
        return;
    }
    
    container.innerHTML = selectedFoods.map(food => `
        <div class="d-flex justify-content-between align-items-center p-2 border-bottom">
            <div class="flex-grow-1">
                <strong>${food.nombre}</strong>
                <div class="small text-muted">
                    Total: ${formatCurrency(food.costo * food.cantidad)} | ${(food.kcal * food.cantidad).toFixed(0)} kcal
                </div>
            </div>
            <div class="d-flex align-items-center" style="gap: 8px;">
                <input type="number" min="1" value="${food.cantidad}" 
                    class="form-control form-control-sm" style="width: 70px;"
                    onchange="updateQuantity(${food.id}, this.value)">
                <button class="btn btn-sm btn-outline-danger" onclick="removeFood(${food.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join("");
}

function updateNutrition() {
    const totalCalorias = selectedFoods.reduce((sum, f) => sum + (f.kcal * f.cantidad), 0);
    const totalProteinas = selectedFoods.reduce((sum, f) => sum + (f.proteinas * f.cantidad), 0);
    const totalCarbos = selectedFoods.reduce((sum, f) => sum + (f.carbos * f.cantidad), 0);
    const totalCosto = selectedFoods.reduce((sum, f) => sum + (f.costo * f.cantidad), 0); // Cálculo de Costo

    
    document.getElementById("totalCalorias").textContent = `${totalCalorias.toFixed(1)} kcal`;
    document.getElementById("totalProteinas").textContent = `${totalProteinas.toFixed(1)} g`;
    document.getElementById("totalCarbos").textContent = `${totalCarbos.toFixed(1)} g`;
    document.getElementById("totalCosto").textContent = formatCurrency(totalCosto); // Mostrar Costo

    // Lógica de validación de restricciones (RF4)
    const alertasContainer = document.getElementById("alertasRestriccion");
    const alertas = [];
    
    if (restricciones.length > 0) {
        // 1. Validar Alergias (CRÍTICO - ALERTA ROJA)
        restricciones.filter(r => r.tipo === "alergia").forEach(r => {
            if (selectedFoods.some(f => f.id === r.alimento_id)) {
                const alimentoAlergico = foods.find(f => f.id === r.alimento_id)?.nombre || "Alimento prohibido";
                alertas.push(`<div class="alert alert-danger p-2 mb-2" role="alert"><i class="fas fa-exclamation-triangle me-1"></i> ALERGIA CRÍTICA: Contiene ${alimentoAlergico}.</div>`);
            }
        });

        // 2. Validar Prohibidos por texto (ADVERTENCIA)
        const textosProhibidos = restricciones.filter(r => r.tipo === "prohibido" && r.texto).map(r => r.texto.toLowerCase());
        selectedFoods.forEach(f => {
            if (textosProhibidos.some(t => f.nombre.toLowerCase().includes(t))) {
                alertas.push(`<div class="alert alert-warning p-2 mb-2" role="alert"><i class="fas fa-exclamation-triangle me-1"></i> Advertencia: El alimento ${f.nombre} podría contener ${textosProhibidos.join(", ")}.</div>`);
            }
        });
    }

    // 3. Alertas Nutricionales (UX)
    if (totalCalorias > 500) {
        alertas.push(`<div class="alert alert-info p-2 mb-2" role="alert"><i class="fas fa-balance-scale me-1"></i> La lonchera supera las 500 kcal recomendadas.</div>`);
    } else if (totalCalorias < 200 && totalCalorias > 0) {
        alertas.push(`<div class="alert alert-info p-2 mb-2" role="alert"><i class="fas fa-balance-scale me-1"></i> Bajo contenido calórico (menos de 200 kcal).</div>`);
    }

    alertasContainer.innerHTML = alertas.join("");
}

async function createLunchbox() {
    const hijoId = document.getElementById("hijoSelect").value;
    const fecha = document.getElementById("fechaInput").value;
    const direccionId = document.getElementById("direccionSelect").value || null;
    
    if (!hijoId || !fecha || selectedFoods.length === 0) {
        showNotification("Error", "Debes completar Hijo, Fecha y agregar alimentos", "warning");
        return;
    }
    
    // Alerta crítica de alergia antes de crear
    const tieneAlergiaCritica = restricciones.filter(r => r.tipo === "alergia").some(r => 
        selectedFoods.some(f => f.id === r.alimento_id)
    );

    if (tieneAlergiaCritica) {
        const result = await confirmAction(
            "¡ALERTA CRÍTICA!",
            "Esta lonchera contiene un alimento que causa ALERGIA grave al niño. ¿Deseas continuar bajo tu responsabilidad?"
        );
        if (!result.isConfirmed) {
            return;
        }
    }
    
    try {
        showLoading();
        
        // 1. Crear lonchera (RF3.1)
        const lunchbox = await API.createLunchbox({
            hijo_id: parseInt(hijoId),
            fecha,
            estado: "Borrador",
            direccion_id: direccionId ? parseInt(direccionId) : null
        });
        
        // 2. Agregar items (LoncheraAlimento)
        for (const food of selectedFoods) {
            await API.addItemToLunchbox(lunchbox.id, {
                alimento_id: food.id,
                cantidad: food.cantidad
            });
        }
        
        closeLoading();
        
        showNotification(
            "¡Éxito!",
            "Lonchera creada correctamente",
            "success"
        );
        
        setTimeout(() => {
            window.location.href = "mis-loncheras.html";
        }, 2000);
        
    } catch (error) {
        closeLoading();
        showNotification("Error", error.message, "error");
    }
}

document.getElementById("searchFood").addEventListener("input", (e) => {
    const search = e.target.value.toLowerCase();
    const filtered = foods.filter(f => 
        f.nombre.toLowerCase().includes(search)
    );
    renderFoods(filtered);
});

loadData();