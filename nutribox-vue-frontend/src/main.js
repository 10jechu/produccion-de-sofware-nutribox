import 'bootstrap/dist/css/bootstrap.min.css'; // Importa CSS de Bootstrap
import './assets/main.css';                     // Importa tu CSS principal (ya debería estar)
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'sweetalert2/dist/sweetalert2.min.css'; // <-- Añade esta línea


const app = createApp(App)

app.use(router)

app.mount('#app')
