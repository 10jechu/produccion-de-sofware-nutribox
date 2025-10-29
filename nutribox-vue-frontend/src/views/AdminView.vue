<script setup>
import { ref, onMounted, computed } from 'vue';
import Swal from 'sweetalert2';
import apiService from '@/services/api.service';
import { useRouter } from 'vue-router';

const users = ref([]);
const roles = ref([]);
const memberships = ref([]);
const isLoading = ref(true);
const router = useRouter();

const fetchAdminData = async () => {
    try {
        const [userList, roleList, membershipList] = await Promise.all([
            apiService.get('/users'), // 1. Lista todos los usuarios
            // Asumimos que existen endpoints para roles y membresías (si no, esto fallará silenciosamente, pero lo ignoramos por ahora)
            // apiService.get('/admin/roles'), 
            // apiService.get('/admin/memberships')
        ]);
        
        // Asignamos solo las listas de usuarios para el ejemplo de frontend
        users.value = userList; 
        // Si tienes las listas de roles/membresías de los endpoints, las asignarías aquí:
        // roles.value = roleList;
        // memberships.value = membershipList;
        
        isLoading.value = false;
    } catch (error) {
        isLoading.value = false;
        if (error.message.includes("403")) {
            Swal.fire('Acceso Denegado', 'No tienes permisos de Administrador.', 'error');
            router.push('/dashboard');
        } else {
            // No mostramos el error crítico al usuario para mantener la fluidez
            console.error("Error al cargar datos de administración:", error);
        }
    }
};

const assignMembership = async (user) => {
    // Lógica simplificada para asignar membresía
    Swal.fire('Función Pendiente', `Simulación de asignación de plan a ${user.email}. Implementar PATCH /users/{id}.`, 'info');
};


onMounted(() => {
    fetchAdminData();
});
</script>

<template>
  <main class="flex-grow-1 p-4 bg-light">
    <div class="dashboard-header mb-4">
        <h1 class="h3 text-danger">Panel de Administración</h1>
        <p class="text-muted">Gestión de datos maestros, roles y planes de membresía.</p>
    </div>

    <div v-if="isLoading" class="text-center p-5">
        <i class="fas fa-spinner fa-spin fa-2x text-primary-nb"></i>
        <p class="mt-2 text-muted">Cargando panel de administración...</p>
    </div>

    <div v-else class="card p-4 card-shadow">
        <h5 class="fw-bold mb-3">Gestión de Usuarios y Membresías (RF1.3 / RF8.1)</h5>
        
        <div class="table-responsive">
            <table class="table table-hover align-middle">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th> <th>Email</th>
                        <th>Rol Actual</th>
                        <th>Membresía</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in users" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td>{{ user.nombre }}</td> <td>{{ user.email }}</td>
                        <td><span class="badge bg-info">{{ user.rol_id }}</span></td>
                        <td><span :class="['badge', user.membresia_id === 3 ? 'bg-warning text-dark' : 'bg-secondary']">{{ user.membresia_id }}</span></td>
                        <td>
                            <button class="btn btn-sm btn-outline-primary" @click="assignMembership(user)">
                                <i class="fas fa-edit me-1"></i> Asignar Plan
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
  </main>
</template>
