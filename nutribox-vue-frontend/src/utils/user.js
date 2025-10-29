// <<<<<<<<<< COMIENZA CÓDIGO CORREGIDO PARA nutribox-vue-frontend/src/utils/user.js >>>>>>>>>>

// --- Función para obtener los detalles del usuario desde localStorage ---
// (Asegúrate que esta función ya exista y funcione correctamente)
export function getUserDetail() {
  const userStr = localStorage.getItem('nutribox_user');
  try {
    // Intenta parsear, devuelve null si está vacío o es inválido
    return userStr ? JSON.parse(userStr) : null;
  } catch (e) {
    console.error("Error parsing user detail from localStorage:", e);
    // Limpia el item inválido si falla el parseo
    localStorage.removeItem('nutribox_user');
    return null;
  }
}

// --- Función para verificar si el usuario es Administrador ---
export function isAdmin() {
  const detail = getUserDetail();
  // Forma segura sin optional chaining: verifica cada nivel
  return detail && detail.rol && detail.rol.nombre === 'Admin'; // Asegúrate que 'Admin' sea el nombre correcto
}

// --- Función para verificar si el usuario tiene la membresía requerida (o superior) ---
export function hasRequiredMembership(requiredPlan) {
  const detail = getUserDetail();
  // Forma segura sin optional chaining: verifica cada nivel
  const userPlan = (detail && detail.membresia && detail.membresia.tipo) ? detail.membresia.tipo : 'Free'; // Asume 'Free' por defecto

  // Mapeo de nombres de planes a niveles numéricos
  const tiers = {
    'Básico': 0,
    'Free': 0,
    'Estándar': 1,
    'Estandar': 1, // Incluye posibles variaciones
    'Premium': 2
   };

  // Obtiene el nivel numérico del usuario (o 0 si el plan no se reconoce)
  const userTier = tiers[userPlan] !== undefined ? tiers[userPlan] : 0;
  // Obtiene el nivel numérico requerido (o 0 si no se reconoce)
  const requiredTier = tiers[requiredPlan] !== undefined ? tiers[requiredPlan] : 0;

  // Compara: el nivel del usuario debe ser mayor o igual al requerido
  return userTier >= requiredTier;
}

// <<<<<<<<<< FIN CÓDIGO CORREGIDO PARA nutribox-vue-frontend/src/utils/user.js >>>>>>>>>>