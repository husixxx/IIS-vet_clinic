import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import MainLayout from '../layouts/Mainlayout.vue';  // Import your layout
import Home from '../views/Home.vue';
import About from '../views/About.vue';
import Signin from '../views/Signin_view.vue';
import Animal_info from '../views/Animalinfo_view.vue';
import Signup from '../views/Signup_view.vue';
import Animal from '../views/Animal_view.vue';


const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    component: MainLayout,  // Use MainLayout as the wrapper
    children: [
      {
        path: '',
        name: 'Home',
        component: Home,
      },
      {
        path: 'about',
        name: 'About',
        component: About,
      },
      {
        path: 'signin',
        name: 'Sign',
        component: Signin,
      },
      {
        path: 'signup',
        name: 'Signup',
        component: Signup,
      },
      {
        path: 'animalinfo',
        name: 'Animalinfo',
        component: Animal_info,
      },
      {
        path: 'animal',
        name: 'Animal',
        component: Animal,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;