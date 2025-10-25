// js/auth.js

// Manejar registro
const handleRegister = async (event) => {
    event.preventDefault(); // 🚨 CRÍTICO: Previene la recarga

    const nombre = document.getElementById('nombre').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const membresia = document.getElementById('membresia').value;

    try {
        showLoading();

        const response = await API.register({
            nombre,
            email,
            password,
            membresia,
            rol: 'Usuario'
        });

        closeLoading();

        showNotification(
            '¡Registro exitoso!',
            'Tu cuenta ha sido creada. Ahora puedes iniciar sesión.',
            'success'
        );

        setTimeout(() => {
            window.location.href = 'login.html';
        }, 2000);

    } catch (error) {
        closeLoading();
        showNotification(
            'Error',
            error.message || 'No se pudo completar el registro',
            'error'
        );
    }
};

// Manejar login
const handleLogin = async (event) => {
    event.preventDefault(); // 🚨 CRÍTICO: Previene la recarga

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        showLoading();

        // API.login() ahora guarda el token y el user
        const response = await API.login(email, password);

        closeLoading();

        // Redirigir al dashboard
        window.location.href = 'dashboard.html';

    } catch (error) {
        closeLoading();
        showNotification(
            'Error',
            'Credenciales inválidas',
            'error'
        );
    }
};