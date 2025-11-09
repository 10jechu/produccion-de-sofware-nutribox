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
        userData = await API.getUserDetail(user.id);
        
        // Actualizar UI
        document.getElementById('userName').textContent = userData.nombre;
        document.getElementById('totalHijos').textContent = userData.resumen.total_hijos;
        document.getElementById('totalLoncheras').textContent = userData.resumen.loncheras_este_mes;
        document.getElementById('totalDirecciones').textContent = userData.resumen.total_direcciones;
        
        const planMembresiaText = document.getElementById('planMembresia');
        planMembresiaText.textContent = userData.membresia.tipo;
        document.getElementById('maxDirecciones').textContent = userData.membresia.max_direcciones;
        
        // Estilizar el badge del plan usando la nueva paleta
        const planBadge = document.getElementById('planMembresia');
        planBadge.classList.remove('bg-success', 'bg-warning', 'text-dark', 'bg-info', 'bg-secondary');
        
        if (userData.membresia.tipo === 'Premium') {
            planBadge.classList.add('bg-secondary', 'text-white'); // Usar Naranja Secundario como Premium
        } else if (userData.membresia.tipo === 'Estandar') {
            planBadge.classList.add('bg-accent', 'text-white'); // Usar Azul Acento
        } else {
             planBadge.classList.add('bg-muted', 'text-white'); // Usar Gris Muted
        }
        
        closeLoading();
    } catch (error) {
        closeLoading();
        console.error('Error cargando dashboard:', error);
        // Si hay error en el token (401), forzamos el logout.
        if (error.message.includes("Token inválido") || error.message.includes("Usuario no encontrado")) {
            logout();
            return;
        }
        showNotification('Error', 'No se pudo cargar el dashboard', 'error');
    }
}

loadDashboard();
