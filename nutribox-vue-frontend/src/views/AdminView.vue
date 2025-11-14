<template>
  <main class="flex-grow-1 p-4 bg-light">
    <div class="dashboard-header mb-4">
        <h1 class="h3 text-success">🍃 Panel de Administración</h1>
        <p class="text-muted">Gestión de alimentos y menús del sistema</p>
    </div>

    <!-- Estadísticas Rápidas -->
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card text-center">
          <div class="card-body">
            <i class="fas fa-utensils fa-2x text-primary mb-2"></i>
            <h3>{{ stats.totalFoods }}</h3>
            <p class="text-muted mb-0">Alimentos</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center">
          <div class="card-body">
            <i class="fas fa-book-open fa-2x text-success mb-2"></i>
            <h3>{{ stats.totalMenus }}</h3>
            <p class="text-muted mb-0">Menús</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-center">
          <div class="card-body">
            <i class="fas fa-users fa-2x text-warning mb-2"></i>
            <h3>{{ stats.totalUsers }}</h3>
            <p class="text-muted mb-0">Usuarios</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Pestañas para Alimentos y Menús -->
    <div class="card">
      <div class="card-header">
        <ul class="nav nav-tabs card-header-tabs">
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activeTab === 'foods' }"
                    @click="activeTab = 'foods'">
              <i class="fas fa-utensils me-2"></i>Gestionar Alimentos
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activeTab === 'menus' }"
                    @click="activeTab = 'menus'">
              <i class="fas fa-book-open me-2"></i>Gestionar Menús
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" :class="{ active: activeTab === 'users' }"
                    @click="activeTab = 'users'">
              <i class="fas fa-users me-2"></i>Usuarios Registrados
            </button>
          </li>
        </ul>
      </div>

      <div class="card-body">
        <!-- Tabla de Alimentos -->
        <div v-if="activeTab === 'foods'">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5>Lista de Alimentos del Sistema</h5>
            <button class="btn btn-success btn-sm" @click="goToFoods">
              <i class="fas fa-utensils me-1"></i>Gestionar Alimentos
            </button>
          </div>

          <div v-if="isLoading" class="text-center p-4">
            <i class="fas fa-spinner fa-spin fa-2x text-primary"></i>
            <p class="mt-2 text-muted">Cargando alimentos...</p>
          </div>

          <div v-else class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Calorías</th>
                  <th>Proteínas</th>
                  <th>Carbohidratos</th>
                  <th>Costo</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="food in foods" :key="food.id">
                  <td>{{ food.nombre }}</td>
                  <td>{{ food.kcal }} kcal</td>
                  <td>{{ food.proteinas }}g</td>
                  <td>{{ food.carbos }}g</td>
                  <td>{{ formatPrice(food.costo) }}</td>
                  <td>
                    <span :class="food.activo ? 'badge bg-success' : 'badge bg-secondary'">
                      {{ food.activo ? 'Activo' : 'Inactivo' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Tabla de Menús -->
        <div v-if="activeTab === 'menus'">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5>Menús Predeterminados</h5>
            <button class="btn btn-success btn-sm" @click="goToMenus">
              <i class="fas fa-book-open me-1"></i>Gestionar Menús
            </button>
          </div>

          <div v-if="isLoading" class="text-center p-4">
            <i class="fas fa-spinner fa-spin fa-2x text-primary"></i>
            <p class="mt-2 text-muted">Cargando menús...</p>
          </div>

          <div v-else class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Fecha</th>
                  <th>Estado</th>
                  <th>Hijo ID</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="menu in menus" :key="menu.id">
                  <td>{{ menu.id }}</td>
                  <td>{{ formatDate(menu.fecha) }}</td>
                  <td>
                    <span :class="getStatusBadgeClass(menu.estado)" class="badge">
                      {{ menu.estado }}
                    </span>
                  </td>
                  <td>{{ menu.hijo_id }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Tabla de Usuarios -->
        <div v-if="activeTab === 'users'">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5>Usuarios Registrados</h5>
            <button class="btn btn-primary btn-sm" @click="loadUsers">
              <i class="fas fa-refresh me-1"></i>Actualizar
            </button>
          </div>

          <div v-if="isLoading" class="text-center p-4">
            <i class="fas fa-spinner fa-spin fa-2x text-primary"></i>
            <p class="mt-2 text-muted">Cargando usuarios...</p>
          </div>

          <div v-else class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nombre</th>
                  <th>Email</th>
                  <th>Estado</th>
                  <th>Rol</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>{{ user.nombre }}</td>
                  <td>{{ user.email }}</td>
                  <td>
                    <span :class="user.activo ? 'badge bg-success' : 'badge bg-secondary'">
                      {{ user.activo ? 'Activo' : 'Inactivo' }}
                    </span>
                  </td>
                  <td>
                    <span class="badge bg-info">{{ user.rol?.nombre || 'Usuario' }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';

const router = useRouter();

const activeTab = ref('foods');
const foods = ref([]);
const menus = ref([]);
const users = ref([]);
const isLoading = ref(true);
const stats = ref({
  totalFoods: 0,
  totalMenus: 0,
  totalUsers: 0
});

const formatPrice = (price) => {
  return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(price || 0);
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-CO');
};

const getStatusBadgeClass = (status) => {
  const classes = {
    'Borrador': 'bg-warning text-dark',
    'Confirmada': 'bg-success',
    'Entregada': 'bg-info',
    'Cancelada': 'bg-danger'
  };
  return classes[status] || 'bg-secondary';
};

const loadFoods = async () => {
  try {
    const foodList = await apiService.get('/foods');
    foods.value = foodList;
    stats.value.totalFoods = foodList.length;
  } catch (error) {
    console.error('Error cargando alimentos:', error);
    Swal.fire('Error', 'No se pudieron cargar los alimentos', 'error');
  }
};

const loadMenus = async () => {
  try {
    const menuList = await apiService.get('/menus');
    menus.value = menuList;
    stats.value.totalMenus = menuList.length;
  } catch (error) {
    console.error('Error cargando menús:', error);
    // No mostrar error si no hay menús
  }
};

const loadUsers = async () => {
  try {
    const userList = await apiService.get('/users');
    users.value = userList;
    stats.value.totalUsers = userList.length;
  } catch (error) {
    console.error('Error cargando usuarios:', error);
    Swal.fire('Error', 'No se pudieron cargar los usuarios', 'error');
  }
};

const loadAdminData = async () => {
  isLoading.value = true;
  await Promise.all([loadFoods(), loadMenus(), loadUsers()]);
  isLoading.value = false;
};

const goToFoods = () => {
  router.push('/app/alimentos');
};

const goToMenus = () => {
  router.push('/app/menus');
};

onMounted(() => {
  loadAdminData();
});
</script>

<style scoped>
.nav-tabs .nav-link.active {
  background-color: #1F8D45;
  color: white;
  border-color: #1F8D45;
}

.table th {
  background-color: #f8f9fa;
  border-top: none;
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}
</style>