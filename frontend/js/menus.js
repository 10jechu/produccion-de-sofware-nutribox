requireAuth();

async function loadMenus() {
    try {
        showLoading();
        // Simulación: Cargamos loncheras creadas por un usuario "Admin" (ID 1)
        // En un caso real, esto vendría de un endpoint /menus
        const allLunchboxes = await API.getLunchboxes();
        const user = getUser();
        
        // Aquí simulamos que los menús son loncheras NO pertenecientes al usuario actual
        // En una implementación real, tendrías un flag o un endpoint específico
        const menus = allLunchboxes.filter(lb => lb.usuario_id !== user.id);

        renderMenus(menus, user);
        closeLoading();
    } catch (error) {
        closeLoading();
        showNotification("Error", "No se pudieron cargar los menús.", "error");
    }
}

function renderMenus(menus, currentUser) {
    const container = document.getElementById("menusContainer");
    const userPlan = currentUser.membresia.tipo; // Asumiendo que 'membresia' está en el objeto de usuario

    if (menus.length === 0) {
        container.innerHTML = `<div class="col-12"><div class="card p-5 text-center">No hay menús predeterminados disponibles en este momento.</div></div>`;
        return;
    }

    container.innerHTML = menus.map(menu => {
        // Lógica de botones según el plan
        let actionButton = '';
        if (userPlan === 'Estandar' || userPlan === 'Premium') {
            actionButton = `<button class="btn btn-primary-nb w-100" onclick="addMenuToProfile(${menu.id})">Agregar a Mis Loncheras</button>`;
        } else { // Plan Básico
            actionButton = `<button class="btn btn-secondary w-100" disabled>Disponible en Plan Estándar</button>`;
        }

        return `
            <div class="col-md-4">
                <div class="card h-100 card-shadow">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title fw-bold">Menú #${menu.id}</h5>
                        <p class="card-text text-muted">Una selección balanceada para empezar.</p>
                        <ul class="list-unstyled mt-3 mb-4">
                           <li><i class="fas fa-check text-success me-2"></i> Nutritivo y delicioso</li>
                           <li><i class="fas fa-check text-success me-2"></i> Aprobado por expertos</li>
                        </ul>
                        <div class="mt-auto">
                            ${actionButton}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join("");
}

async function addMenuToProfile(menuId) {
    // Esta función es una simulación.
    // La lógica real implicaría copiar la lonchera (menu) al perfil del usuario actual.
    showNotification("Función Simulada", "En una implementación completa, este menú se copiaría a 'Mis Loncheras'.", "info");
}

loadMenus();