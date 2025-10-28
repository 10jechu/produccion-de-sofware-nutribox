requireAuth();

async function loadProfile() {
    try {
        showLoading();
        const user = getUser();
        
        if (!user) {
            logout();
            return;
        }
        
        const detail = await API.getUserDetail(user.id);
        
        document.getElementById("userName").textContent = detail.nombre;
        document.getElementById("userEmail").textContent = detail.email;
        document.getElementById("userRole").textContent = detail.rol.nombre;
        document.getElementById("userMembership").textContent = detail.membresia.tipo;
        document.getElementById("totalHijos").textContent = detail.resumen.total_hijos;
        document.getElementById("totalDirecciones").textContent = detail.resumen.total_direcciones;
        
        // Estilizar el badge del plan
        const planBadge = document.getElementById('userMembership');
        if (detail.membresia.tipo === 'Premium') {
            planBadge.classList.add('bg-warning', 'text-dark');
        } else if (detail.membresia.tipo === 'Estandar') {
            planBadge.classList.add('bg-info');
        } else {
             planBadge.classList.add('bg-secondary');
        }
        
        closeLoading();
    } catch (error) {
        closeLoading();
         if (error.message.includes("Token inválido")) {
            logout();
            return;
        }
        showNotification("Error", "No se pudo cargar el perfil", "error");
    }
}

function showEditProfileModal() {
    showNotification("Función No Implementada", "La edición de perfil está pendiente.", "info");
}

loadProfile();