// Función para obtener los detalles del usuario desde localStorage
export function getUserDetail() {
  const userStr = localStorage.getItem('nutribox_user');
  try {
    return userStr ? JSON.parse(userStr) : null;
  } catch (e) {
    console.error("Error parsing user detail from localStorage:", e);
    localStorage.removeItem('nutribox_user');
    return null;
  }
}

// Función para verificar si el usuario es Administrador
export function isAdmin() {
  const detail = getUserDetail();
  // Compatible con la estructura real del backend
  return detail && detail.rol && detail.rol.nombre === 'Admin';
}

// Función para verificar si el usuario tiene la membresía requerida (o superior)
export function hasRequiredMembership(requiredPlan) {
  const detail = getUserDetail();
  
  // Compatible con la estructura real del backend
  const userPlan = (detail && detail.membresia && detail.membresia.tipo) ? detail.membresia.tipo : 'Free';

  // Mapeo de nombres de planes a niveles numéricos
  const tiers = {
    'Free': 0,
    'Estandar': 1,
    'Premium': 2
  };

  // Obtiene el nivel numérico del usuario (o 0 si el plan no se reconoce)
  const userTier = tiers[userPlan] !== undefined ? tiers[userPlan] : 0;
  // Obtiene el nivel numérico requerido (o 0 si no se reconoce)
  const requiredTier = tiers[requiredPlan] !== undefined ? tiers[requiredPlan] : 0;

  // Compara: el nivel del usuario debe ser mayor o igual al requerido
  return userTier >= requiredTier;
}

// Función para verificar si el usuario puede crear loncheras
export function canCreateLunchboxes() {
  return hasRequiredMembership('Estandar');
}

// Función para verificar si el usuario puede ver historial (Premium)
export function canViewHistory() {
  return hasRequiredMembership('Premium');
}

// Función para obtener el límite de direcciones del usuario
export function getAddressLimit() {
  const detail = getUserDetail();
  if (detail && detail.membresia && detail.membresia.max_direcciones) {
    return detail.membresia.max_direcciones;
  }
  return 1; // Default
}