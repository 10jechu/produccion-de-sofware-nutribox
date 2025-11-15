<template>
  <main class="flex-grow-1 p-4 bg-light">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h1 class="h3">Alimentos</h1>
        <p class="text-muted">Gestiona los alimentos del sistema</p>
      </div>
      <button v-if="isUserAdmin" class="btn btn-success" @click="showCreateModal = true">
        <i class="fas fa-plus me-1"></i> Agregar Alimento
      </button>
    </div>

    <!-- Búsqueda -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-8">
            <input 
              v-model="searchQuery" 
              type="text" 
              class="form-control" 
              placeholder="Buscar alimentos por nombre..."
              @input="searchFoods"
            >
          </div>
          <div class="col-md-4">
            <button class="btn btn-outline-secondary w-100" @click="clearFilters">
              <i class="fas fa-times me-1"></i> Limpiar
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="text-center p-5">
      <i class="fas fa-spinner fa-spin fa-2x text-primary"></i>
      <p class="mt-2 text-muted">Cargando alimentos...</p>
    </div>

    <!-- Tabla de Alimentos -->
    <div v-else class="card">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Calorías</th>
                <th>Proteínas (g)</th>
                <th>Carbohidratos (g)</th>
                <th>Costo (COP)</th>
                <th>Estado</th>
                <th v-if="isUserAdmin">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="food in filteredFoods" :key="food.id">
                <td>
                  <strong>{{ food.nombre }}</strong>
                </td>
                <td>
                  <span class="text-warning fw-bold">{{ food.kcal || 0 }} kcal</span>
                </td>
                <td>{{ food.proteinas || 0 }}g</td>
                <td>{{ food.carbos || 0 }}g</td>
                <td>
                  <strong class="text-success">{{ formatPrice(food.costo) }}</strong>
                </td>
                <td>
                  <span :class="food.activo ? 'badge bg-success' : 'badge bg-secondary'">
                    {{ food.activo ? 'Activo' : 'Inactivo' }}
                  </span>
                </td>
                <td v-if="isUserAdmin">
                  <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" @click="editFood(food)" title="Editar">
                      <i class="fas fa-edit"></i>
                    </button>
                    <button 
                      class="btn" 
                      :class="food.activo ? 'btn-outline-danger' : 'btn-outline-warning'" 
                      @click="food.activo ? deleteFood(food) : activateFood(food)" 
                      :title="food.activo ? 'Desactivar' : 'Activar'"
                    >
                      <i :class="food.activo ? 'fas fa-times' : 'fas fa-check'"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Mensaje sin resultados -->
        <div v-if="filteredFoods.length === 0 && !isLoading" class="text-center p-5">
          <i class="fas fa-search fa-2x text-muted mb-3"></i>
          <h5>No se encontraron alimentos</h5>
          <p class="text-muted">Intenta con otros términos de búsqueda</p>
          <button v-if="isUserAdmin" class="btn btn-success mt-2" @click="showCreateModal = true">
            <i class="fas fa-plus me-1"></i> Crear Primer Alimento
          </button>
        </div>
      </div>
    </div>

    <!-- Modal para Crear/Editar Alimento -->
    <div v-if="showCreateModal" class="modal fade show d-block" style="background-color: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingFood ? 'Editar' : 'Crear' }} Alimento</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveFood">
              <div class="row g-3">
                <div class="col-12">
                  <label class="form-label">Nombre *</label>
                  <input v-model="foodForm.nombre" type="text" class="form-control" required>
                </div>
                
                <div class="col-md-4">
                  <label class="form-label">Calorías (kcal) *</label>
                  <input v-model.number="foodForm.kcal" type="number" class="form-control" min="0" step="0.1" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Proteínas (g) *</label>
                  <input v-model.number="foodForm.proteinas" type="number" class="form-control" min="0" step="0.1" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Carbohidratos (g) *</label>
                  <input v-model.number="foodForm.carbos" type="number" class="form-control" min="0" step="0.1" required>
                </div>
                
                <div class="col-12">
                  <label class="form-label">Costo (COP) *</label>
                  <input v-model.number="foodForm.costo" type="number" class="form-control" min="0" step="100" required>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancelar</button>
            <button type="button" class="btn btn-success" @click="saveFood" :disabled="saving">
              <i v-if="saving" class="fas fa-spinner fa-spin me-1"></i>
              {{ saving ? 'Guardando...' : (editingFood ? 'Actualizar' : 'Crear') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { getUserDetail, isAdmin } from '@/utils/user';

const foods = ref([]);
const filteredFoods = ref([]);
const isLoading = ref(true);
const saving = ref(false);
const showCreateModal = ref(false);
const editingFood = ref(null);
const searchQuery = ref('');

const isUserAdmin = computed(() => isAdmin());

// Formulario de alimento - Sincronizado con backend
const foodForm = ref({
  nombre: '',
  kcal: 0,
  proteinas: 0,
  carbos: 0,
  costo: 0
});

const formatPrice = (price) => {
  return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(price || 0);
};

// Cargar alimentos
const loadFoods = async () => {
  try {
    isLoading.value = true;
    
    const foodList = await apiService.get('/foods');
    foods.value = foodList;
    filteredFoods.value = foodList;
    
  } catch (error) {
    console.error('❌ Error cargando alimentos:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.message || 'No se pudieron cargar los alimentos'
    });
    foods.value = [];
    filteredFoods.value = [];
  } finally {
    isLoading.value = false;
  }
};

// Buscar alimentos
const searchFoods = () => {
  if (!searchQuery.value) {
    filteredFoods.value = foods.value;
    return;
  }

  const query = searchQuery.value.toLowerCase();
  filteredFoods.value = foods.value.filter(food => 
    food.nombre.toLowerCase().includes(query)
  );
};

const clearFilters = () => {
  searchQuery.value = '';
  filteredFoods.value = foods.value;
};

// CRUD Operations
const createFood = () => {
  editingFood.value = null;
  foodForm.value = {
    nombre: '',
    kcal: 0,
    proteinas: 0,
    carbos: 0,
    costo: 0
  };
  showCreateModal.value = true;
};

const editFood = (food) => {
  editingFood.value = food;
  foodForm.value = { ...food };
  showCreateModal.value = true;
};

const saveFood = async () => {
  try {
    saving.value = true;

    // Validaciones básicas
    if (!foodForm.value.nombre.trim()) {
      throw new Error('El nombre es requerido');
    }
    if (foodForm.value.kcal <= 0) {
      throw new Error('Las calorías deben ser mayores a 0');
    }
    if (foodForm.value.costo < 0) {
      throw new Error('El costo no puede ser negativo');
    }

    if (editingFood.value) {
      // ✅ CORREGIDO: Usar PATCH en vez de PUT
      await apiService.patch(`/foods/${editingFood.value.id}`, foodForm.value);
      Swal.fire('¡Éxito!', 'Alimento actualizado correctamente', 'success');
    } else {
      // Crear nuevo alimento
      await apiService.post('/foods', foodForm.value);
      Swal.fire('¡Éxito!', 'Alimento creado correctamente', 'success');
    }

    await loadFoods();
    closeModal();
    
  } catch (error) {
    console.error('❌ Error guardando alimento:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.message || 'No se pudo guardar el alimento'
    });
  } finally {
    saving.value = false;
  }
};

const deleteFood = async (food) => {
  const result = await Swal.fire({
    title: `¿Desactivar "${food.nombre}"?`,
    text: 'El alimento ya no estará disponible para nuevas loncheras',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Sí, desactivar',
    cancelButtonText: 'Cancelar'
  });

  if (result.isConfirmed) {
    try {
      Swal.showLoading();
      
      await apiService.delete(`/foods/${food.id}`);
      
      Swal.close();
      Swal.fire('¡Desactivado!', 'Alimento desactivado correctamente', 'success');
      await loadFoods();
      
    } catch (error) {
      Swal.close();
      console.error('❌ Error desactivando alimento:', error);
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: error.message || 'No se pudo desactivar el alimento'
      });
    }
  }
};

const activateFood = async (food) => {
  try {
    Swal.showLoading();
    
    // ✅ CORREGIDO: Usar PATCH para activar
    await apiService.patch(`/foods/${food.id}`, { activo: true });
    
    Swal.close();
    Swal.fire('¡Activado!', 'Alimento activado correctamente', 'success');
    await loadFoods();
    
  } catch (error) {
    Swal.close();
    console.error('❌ Error activando alimento:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.message || 'No se pudo activar el alimento'
    });
  }
};

const closeModal = () => {
  showCreateModal.value = false;
  editingFood.value = null;
};

onMounted(() => {
  loadFoods();
});
</script>

<style scoped>
.modal {
  background-color: rgba(0,0,0,0.5);
}

.table th {
  background-color: #f8f9fa;
  border-top: none;
  font-weight: 600;
}

.badge {
  font-size: 0.75em;
}

.btn-group-sm > .btn {
  padding: 0.25rem 0.5rem;
}
</style>