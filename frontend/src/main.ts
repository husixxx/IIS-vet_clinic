import { createApp } from 'vue';
import './assets/style.css';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import router from './routes/routes';  // Import the router from your routes file
import { createPinia } from 'pinia';

const app = createApp(App);
const pinia = createPinia();

// Use PrimeVue with the selected theme
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.use(pinia);

// Add the router to the app so it can handle route navigation
app.use(router);

// Mount the app to the DOM
app.mount('#app');
