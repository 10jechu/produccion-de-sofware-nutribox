<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { isAdmin } from '@/utils/user'; 

const foods = ref([]);
const isLoading = ref(true);

const isUserAdmin = computed(() => isAdmin()); 

function formatCurrency(value) {
    return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(value);
}

async function loadFoods() {
    isLoading.value = true;
    try {
        const filter = isUserAdmin.value ? 'all' : 'true';
        // SINTAXIS CORREGIDA: Concatenacion
        foods.value = await apiService.get('/foods?only_active=' + filter); 
        isLoading.value = false;
    } catch (error) {
        isLoading.value = false;
        Swal.fire('Error', error.message || 'No se pudieron cargar los alimentos', 'error');
    }
}

onMounted(() => {
    loadFoods();
});

const handleFoodAction = (action) => {
    Swal.fire('Funcion de Administrador', 'El CRUD de alimentos (' + action + ') debe implementarse en la vista AdminView.vue para el rol ' + (isUserAdmin.value ? 'Admin' : 'Usuario') + '.', 'info');
}
</script>

<template>
    <main class="flex-grow-1 p-4 bg-light">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div>
                <h1 class="h3">Catalogo de Alimentos</h1>
                <p class="text-muted">Consulta la informacion nutricional y el costo unitario de cada alimento.</p>
            </div>
            <button v-if="isUserAdmin" class="btn btn-primary-nb" @click="handleFoodAction('Agregar')">
                <i class="fas fa-plus me-1"></i> Agregar Alimento (Admin)
            </button>
        </div>

        <div class="card p-4 card-shadow">
            <div v-if="isLoading" class="text-center p-5">
                <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
                <p class="mt-2 text-muted">Cargando catalogo...</p>
            </div>
            
            <div v-else class="table-responsive">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Calorias (kcal)</th>
                            <th>Proteinas (g)</th>
                            <th>Carbohidratos (g)</th>
                            <th>Costo Unitario</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody id="foodsTableBody">
                        <tr v-for="food in foods" :key="food.id">
                            <td>{{ food.nombre }} <span v-if="isUserAdmin && !food.activo" class="badge bg-danger">INACTIVO</span></td>
                            <td>{{ food.kcal }} kcal</td>
                            <td>{{ food.proteinas }} g</td>
                            <td>{{ food.carbos }} g</td>
                            <td>{{ formatCurrency(food.costo) }}</td>
                            <td>
                                <button class="btn btn-sm btn-outline-info me-1" @click="handleFoodAction('Ver Detalle')">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <span v-if="isUserAdmin">
                                    <button class="btn btn-sm btn-outline-warning me-1" @click="handleFoodAction('Editar')"><i class="fas fa-edit"></i></button>
                                    <button class="btn btn-sm btn-outline-danger" @click="handleFoodAction('Eliminar')"><i class="fas fa-trash"></i></button>
                                </span>
                            </td>
                        </tr>
                        <tr v-if="foods.length === 0">
                             <td colspan="6" class="text-center text-muted">No hay alimentos activos en el catalogo.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
</template>