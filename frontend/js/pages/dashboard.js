// Verificar autenticación
requireAuth();

let userData = null;

// Cargar datos del dashboard
async function loadDashboard() {
    try {
        showLoading();
        
        const user = getUser();
        if (!user) {
            logout();
            return;
        }
        
        // Cargar detalle completo del usuario
        userData = await API.getUserDetail(user.id);
        
        // Actualizar UI
        document.getElementById('userName').textContent = userData.nombre;
        document.getElementById('totalHijos').textContent = userData.resumen.total_hijos;
        document.getElementById('totalLoncheras').textContent = userData.resumen.loncheras_este_mes;
        document.getElementById('totalDirecciones').textContent = userData.resumen.total_direcciones;
        document.getElementById('planMembresia').textContent = userData.membresia.tipo;
        document.getElementById('maxDirecciones').textContent = userData.membresia.max_direcciones;
        
        closeLoading();
    } catch (error) {
        closeLoading();
        console.error('Error cargando dashboard:', error);
        showNotification('Error', 'No se pudo cargar el dashboard', 'error');
    }
}

// Cargar al iniciar
loadDashboard();
