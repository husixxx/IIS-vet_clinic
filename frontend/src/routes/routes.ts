import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import MainLayout from '../layouts/Mainlayout.vue';  // Import your layout
import Home from '../views/Home.vue';
import About from '../views/About.vue';
import Signin from '../views/Signin_view.vue';
import Animal_info from '../views/Animalinfo_view.vue';
import Signup from '../views/Signup_view.vue';
import Animal from '../views/Animal_view.vue';
import Create_animal from '../views/CreateAnimal_view.vue'
import { useAuthStore, UserRole } from '../store/Authstore';  // Import AuthStore to access user data
import Approve_volunteer from '../views/ApproveVolunteer_view.vue'


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
        meta: { requiresAuth: true, role: UserRole.Caretaker }  // Only allow access for Caretaker
      },
      {
        path: 'approvevolunteer',
        name: 'ApproveVolunteer',
        component: Approve_volunteer,
        meta: { requiresAuth: true, role: UserRole.Caretaker }  // Only allow access for Caretaker
      }
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  // Check if the route requires authentication and role
  if (to.meta.requiresAuth) {
    if (!authStore.isLoggedIn) {
      // If user is not logged in, redirect to Sign In
      return next({ name: 'Sign' });
    } else if (to.meta.role && authStore.getRoleId !== to.meta.role) {
      // If user's role doesn't match, redirect to Home
      return next({ name: 'Home' });
    }
  }
  next();  // Allow access if no restrictions
});


export default router;
