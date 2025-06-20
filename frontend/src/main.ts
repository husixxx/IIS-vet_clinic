import { createApp } from 'vue';
import './assets/style.css';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import router from './routes/routes';  // Import the router from your routes file
import { createPinia } from 'pinia';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';

const app = createApp(App);
const pinia = createPinia();
// Define the emit event

// Use PrimeVue with the selected theme
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.use(pinia);

// Add the router to the app so it can handle route navigation
app.use(router);
app.use(ToastService);

app.use(ConfirmationService);

// Mount the app to the DOM
app.mount('#app');
