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
                <button class="btn btn-sm btn-outline-info" onclick="viewFoodDetail(${food.id})">
                    <i class="fas fa-eye"></i> Ver Detalle
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

loadFoods();