import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import MainLayout from '../layouts/Mainlayout.vue';  // Import your layout
import Home from '../views/Home.vue';
import About from '../views/About.vue';
import Signin from '../views/Signin_view.vue';
import Animal_info from '../views/Animalinfo_view.vue';
import Signup from '../views/Signup_view.vue';
import Animal from '../views/Animal_view.vue';
import Create_animal from '../views/CreateAnimal_view.vue'
import { useAuthStore } from '../store/Authstore';  // Import AuthStore to access user data


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
      {
        path: 'createanimal',
        name: 'CreateAnimal',
        component: Create_animal,
        beforeEnter: (to, from, next) => {  // Correct use of `next` function
          const authStore = useAuthStore();  // Access the AuthStore
          const user = authStore.getUser;  // Get the logged-in user
          
          // Check if the user exists and has the correct role
          if (user && user.role_id === 3) {
            next();  // User has access, allow navigation
          } else {
            alert("You do not have permission to access this page.");  // Show alert or handle the error
            next({ name: 'Home' });  // Redirect to Home or Signin
          }
        }
      }
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;