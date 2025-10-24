requireAuth();

let foods = [];
let selectedFoods = [];
let hijos = [];
let direcciones = [];

async function loadData() {
    try {
        showLoading();
        const user = getUser();
        
        // Cargar datos en paralelo
        [foods, hijos, direcciones] = await Promise.all([
            API.getFoods('true'),
            API.getChildren(user.id),
            API.getAddresses(user.id)
        ]);
        
        populateSelects();
        renderFoods();
        
        // Establecer fecha mínima (hoy)
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('fechaInput').min = today;
        document.getElementById('fechaInput').value = today;
        
        closeLoading();
    } catch (error) {
        closeLoading();
        showNotification('Error', 'No se pudieron cargar los datos', 'error');
    }
}

function populateSelects() {
    const hijoSelect = document.getElementById('hijoSelect');
    const direccionSelect = document.getElementById('direccionSelect');
    
    hijoSelect.innerHTML = '<option value="">Selecciona un hijo</option>' +
        hijos.map(h => `<option value="${h.id}">${h.nombre}</option>`).join('');
    
    direccionSelect.innerHTML = '<option value="">Selecciona una dirección (opcional)</option>' +
        direcciones.map(d => `<option value="${d.id}">${d.etiqueta} - ${d.direccion}</option>`).join('');
}

function renderFoods() {
    const container = document.getElementById('foodsContainer');
    
    container.innerHTML = foods.map(food => `
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; border-bottom: 1px solid var(--border);">
            <div>
                <strong>${food.nombre}</strong>
                <div style="font-size: 12px; color: var(--text-light);">
                    ${food.kcal} kcal | Prot: ${food.proteinas}g | Carbos: ${food.carbos}g
                </div>
            </div>
            <button class="btn btn-primary" style="padding: 6px 12px;" onclick="addFood(${food.id})">
                <i class="fas fa-plus"></i>
            </button>
        </div>
    `).join('');
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
        food.cantidad = Math.max(1, cantidad);
        renderSelectedFoods();
        updateNutrition();
    }
}

function renderSelectedFoods() {
    const container = document.getElementById('selectedFoodsContainer');
    
    if (selectedFoods.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--text-light);">No hay alimentos seleccionados</p>';
        return;
    }
    
    container.innerHTML = selectedFoods.map(food => `
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; border-bottom: 1px solid var(--border);">
            <div style="flex: 1;">
                <strong>${food.nombre}</strong>
                <div style="font-size: 12px; color: var(--text-light);">
                    ${food.kcal * food.cantidad} kcal
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <input type="number" min="1" value="${food.cantidad}" 
                    style="width: 60px; padding: 4px; border: 1px solid var(--border); border-radius: 4px;"
                    onchange="updateQuantity(${food.id}, this.value)">
                <button class="btn btn-danger" style="padding: 6px 12px;" onclick="removeFood(${food.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

function updateNutrition() {
    const totalCalorias = selectedFoods.reduce((sum, f) => sum + (f.kcal * f.cantidad), 0);
    const totalProteinas = selectedFoods.reduce((sum, f) => sum + (f.proteinas * f.cantidad), 0);
    const totalCarbos = selectedFoods.reduce((sum, f) => sum + (f.carbos * f.cantidad), 0);
    
    document.getElementById('totalCalorias').textContent = `${totalCalorias.toFixed(1)} kcal`;
    document.getElementById('totalProteinas').textContent = `${totalProteinas.toFixed(1)} g`;
    document.getElementById('totalCarbos').textContent = `${totalCarbos.toFixed(1)} g`;
}

async function createLunchbox() {
    const hijoId = document.getElementById('hijoSelect').value;
    const fecha = document.getElementById('fechaInput').value;
    const direccionId = document.getElementById('direccionSelect').value || null;
    
    if (!hijoId) {
        showNotification('Error', 'Debes seleccionar un hijo', 'warning');
        return;
    }
    
    if (!fecha) {
        showNotification('Error', 'Debes seleccionar una fecha', 'warning');
        return;
    }
    
    if (selectedFoods.length === 0) {
        showNotification('Error', 'Debes agregar al menos un alimento', 'warning');
        return;
    }
    
    try {
        showLoading();
        
        // Crear lonchera
        const lunchbox = await API.createLunchbox({
            hijo_id: parseInt(hijoId),
            fecha,
            estado: 'Borrador',
            direccion_id: direccionId ? parseInt(direccionId) : null
        });
        
        // Agregar items
        for (const food of selectedFoods) {
            await API.addItemToLunchbox(lunchbox.id, {
                alimento_id: food.id,
                cantidad: food.cantidad
            });
        }
        
        closeLoading();
        
        showNotification(
            '¡Éxito!',
            'Lonchera creada correctamente',
            'success'
        );
        
        setTimeout(() => {
            window.location.href = 'mis-loncheras.html';
        }, 2000);
        
    } catch (error) {
        closeLoading();
        showNotification('Error', error.message, 'error');
    }
}

// Búsqueda de alimentos
document.getElementById('searchFood').addEventListener('input', (e) => {
    const search = e.target.value.toLowerCase();
    const filtered = foods.filter(f => 
        f.nombre.toLowerCase().includes(search)
    );
    
    const container = document.getElementById('foodsContainer');
    container.innerHTML = filtered.map(food => `
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; border-bottom: 1px solid var(--border);">
            <div>
                <strong>${food.nombre}</strong>
                <div style="font-size: 12px; color: var(--text-light);">
                    ${food.kcal} kcal | Prot: ${food.proteinas}g | Carbos: ${food.carbos}g
                </div>
            </div>
            <button class="btn btn-primary" style="padding: 6px 12px;" onclick="addFood(${food.id})">
                <i class="fas fa-plus"></i>
            </button>
        </div>
    `).join('');
});

loadData();
