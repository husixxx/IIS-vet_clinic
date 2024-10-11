<template>
    <div class="card">
        <Menubar :model="items"/>
    </div>
  </template>
  
<script setup>
import { ref } from "vue";
import { useRouter } from 'vue-router';  // Import the Vue Router hook
import Menubar from 'primevue/menubar';

const router = useRouter();  // Use Vue Router for navigation

const items = ref([
{
    label: 'Home',
    icon: 'pi pi-home',
    command: () => { router.push({name: "Home"}) }  // Route to Home
},
{
    label: 'Animals',
    icon: 'pi pi-paw',
    command: () => { router.push({name: "Animal"}) }  // Route to Animals
},
{
    label: 'About Us',
    icon: 'pi pi-info-circle',
    command: () => { router.push({name: "About"}) }  // Route to About Us
},
{
    label: 'Contact Us',
    icon: 'pi pi-envelope',
    command: () => { router.push({name: "Contact"}) }  // Route to Contact Us
},
{
    label: 'Sign In',
    icon: 'pi pi-sign-in',
    command: () => { router.push({name: "Sign"}) }  // Route to Sign In
}
]);
</script>

  