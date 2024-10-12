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
    command: () => { router.push({name: "Home"}) }  // Route to Home
},
{
    label: 'Animals',
    command: () => { router.push({name: "Animal"}) }  // Route to Animals
},
{
    label: 'About Us',
    command: () => { router.push({name: "About"}) }  // Route to About Us
},
{
    label: 'Contact Us',
    command: () => { router.push({name: "Contact"}) }  // Route to Contact Us
},
{
    label: 'Sign In',
    command: () => { router.push({name: "Sign"}) }  // Route to Sign In
}
]);
</script>

  