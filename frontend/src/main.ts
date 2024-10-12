import { createApp } from 'vue';
import './assets/style.css';
import App from './App.vue';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import router from './routes/routes';  // Import the router from your routes file

const app = createApp(App);

// Use PrimeVue with the selected theme
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});

// Add the router to the app so it can handle route navigation
app.use(router);

// Mount the app to the DOM
app.mount('#app');
