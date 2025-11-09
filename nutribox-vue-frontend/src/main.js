import 'bootstrap/dist/css/bootstrap.min.css'; // Importa CSS de Bootstrap
import './assets/styles.css'; // <-- Importa la nueva hoja de estilos
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'sweetalert2/dist/sweetalert2.min.css';
import '@fortawesome/fontawesome-free/css/all.css'; 

const app = createApp(App)

app.use(router)

app.mount('#app')
