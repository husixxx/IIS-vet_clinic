<template>
    <div class="card">
        <Menubar :model="items" />
    </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from 'vue-router';  // Import the Vue Router hook
import Menubar from 'primevue/menubar';
import { useAuthStore } from '../store/Authstore';  // Import AuthStore

const router = useRouter();  // Use Vue Router for navigation
const authStore = useAuthStore();  // Access the AuthStore

// Base menu items for all users
const items = computed(() => {
    // Get the current user from the store
    const user = authStore.getUser;

    // Base menu items that are always present
    const baseItems = [
        {
            label: 'Home',
            command: () => { router.push({ name: "Home" }) }
        },
        {
            label: 'Animals',
            command: () => { router.push({ name: "Animal" }) }
        },
        {
            label: 'About Us',
            command: () => { router.push({ name: "About" }) }
        }
    ];

    // Add "Actions" dropdown based on role_id
    if (user && [1, 2, 3, 4].includes(user.role_id)) {
        const actions = {
            1: [{ label: 'Request', command: () => {} }],
            2: [{ label: 'Requests', command: () => {} }],
            3: [
                { label: 'Volunteer Approving', command: () => {} },
                { label: 'Create Animal', command: () => { router.push({ name: "CreateAnimal" }) } },
                { label: 'Vet Request', command: () => {} },
                { label: 'Reservation Approving', command: () => {} }
            ],
            4: [
                { label: 'Create Caretaker', command: () => {} },
                { label: 'Create Vet', command: () => {} },
                { label: 'Edit User', command: () => {} }
            ]
        };
        
        // Add the "Actions" dropdown to baseItems
        baseItems.push({
            label: 'Actions',
            items: actions[user.role_id] || []  // Dynamically add items based on role_id
        });
    }
    
    // Check if user is logged in
    if (user) {
        // Add the Logout button when user is logged in
        baseItems.push({
            label: 'Logout',
            command: () => {
                authStore.logout();  // Clear user from AuthStore
                router.push({ name: "Sign" });  // Redirect to Sign In page
            }
        });
    } else {
        // Add the Sign In button when user is not logged in
        baseItems.push({
            label: 'Sign In',
            command: () => { router.push({ name: "Sign" }) }
        });
    }
    return baseItems;
});

</script>
