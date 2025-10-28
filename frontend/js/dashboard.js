// Verificar autenticación
requireAuth();

let userData = null;

async function loadDashboard() {
    try {
        showLoading();
        
        const user = getUser();
        if (!user) {
            logout();
            return;
        }
        
        // Cargar detalle completo del usuario (Contadores, Membresía)
        // La API getUserDetail usa el token para autenticar y el ID para buscar el usuario.
        userData = await API.getUserDetail(user.id);
        
        // Actualizar UI
        document.getElementById('userName').textContent = userData.nombre;
        document.getElementById('totalHijos').textContent = userData.resumen.total_hijos;
        document.getElementById('totalLoncheras').textContent = userData.resumen.loncheras_este_mes;
        document.getElementById('totalDirecciones').textContent = userData.resumen.total_direcciones;
        document.getElementById('planMembresia').textContent = userData.membresia.tipo;
        document.getElementById('maxDirecciones').textContent = userData.membresia.max_direcciones;
        
        // Estilizar el badge del plan
        const planBadge = document.getElementById('planMembresia');
        if (userData.membresia.tipo === 'Premium') {
            planBadge.classList.replace('bg-success', 'bg-warning');
            planBadge.classList.add('text-dark');
        } else if (userData.membresia.tipo === 'Estandar') {
            planBadge.classList.replace('bg-success', 'bg-info');
        } else {
             planBadge.classList.replace('bg-success', 'bg-secondary');
        }
        
        closeLoading();
    } catch (error) {
        closeLoading();
        console.error('Error cargando dashboard:', error);
        // Si hay error en el token (401), forzamos el logout para obtener un nuevo token.
        if (error.message.includes("Token inválido") || error.message.includes("Usuario no encontrado")) {
            logout();
            return;
        }
        showNotification('Error', 'No se pudo cargar el dashboard', 'error');
    }
}

loadDashboard();