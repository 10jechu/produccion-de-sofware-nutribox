// Manejar registro
const handleRegister = async (event) => {
    event.preventDefault();
    
    const nombre = document.getElementById('nombre').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const membresia = document.getElementById('membresia').value;
    
    try {
        showLoading();
        
        await API.register({
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
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        showLoading();
        
        const response = await API.login(email, password);
        
        // Guardar token
        saveToken(response.access_token);
        
        // Obtener datos del usuario
        const users = await API.getUsers(); 
        const user = users.find(u => u.email === email);
        
        if (user) {
            saveUser(user);
        }
        
        closeLoading();
        
        // Redirigir al dashboard (Usamos ruta absoluta para evitar problemas de Live Server)
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
