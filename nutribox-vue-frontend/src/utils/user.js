// nutribox-vue-frontend/src/utils/user.js
// Funciones para obtener información del usuario desde localStorage

export function getUserDetail() {
  const user = localStorage.getItem('nutribox_user');
  return user ? JSON.parse(user) : null;
}

export function hasRequiredMembership(requiredPlan) {
  const detail = getUserDetail();
  if (!detail || !detail.membresia || !detail.membresia.tipo) {
    return false;
  }

  const userPlan = detail.membresia.tipo;

  const tiers = {
    'Free': 0,
    'Estandar': 1,
    'Premium': 2
  };

  const userTier = tiers[userPlan] || 0;
  const requiredTier = tiers[requiredPlan] || 0;

  return userTier >= requiredTier;
}

export function isAdmin() {
  const detail = getUserDetail();
  return detail && detail.rol && detail.rol.nombre === 'Admin';
}
