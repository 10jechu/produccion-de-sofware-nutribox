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

        // Obtener datos del usuario (AHORA OBTENEMOS EL DETALLE COMPLETO)
       try {
            // Primero, obtenemos el usuario básico para sacar el ID
            const users = await API.getUsers();
            const basicUser = users.find(u => u.email === email);

            if (basicUser) {
                // Luego, obtenemos el detalle completo usando el ID
                const detailedUser = await API.getUserDetail(basicUser.id);
                saveUser(detailedUser); // Guardamos el usuario con toda la información
                console.log("Usuario detallado guardado:", detailedUser);
            } else {
                // Manejar caso donde no se encuentra el usuario básico (poco probable si login fue exitoso)
                console.error("No se encontró el usuario básico después del login.");
                throw new Error("Error al obtener datos del usuario.");
            }
        } catch (fetchError) {
            // Manejar errores al obtener el detalle del usuario
            closeLoading();
            console.error("Error al obtener detalle del usuario:", fetchError);
            showNotification(
                'Error',
                'No se pudieron cargar los datos completos del usuario.',
                'error'
            );
            // Podrías decidir si continuar sin guardar user o detener el flujo
            return; // Detiene la ejecución si falla al obtener detalles
        }

        // ESTAS LÍNEAS DEBEN IR DESPUÉS DEL BLOQUE TRY/CATCH ANTERIOR
        closeLoading();
        window.location.href = 'dashboard.html'; // Redirigir al dashboard

    } catch (error) { // Este catch es para el error de API.login
        closeLoading();
        showNotification(
            'Error',
            'Credenciales inválidas', // O usa error.message si prefieres el mensaje de la API
            'error'
        );
    }
};