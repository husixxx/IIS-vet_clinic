<template>
<!-- This will render the component based on the current route -->
<router-view></router-view>
</template>
<script setup>
import { useAuthStore } from './store/Authstore';

const authStore = useAuthStore();

// Synchronizácia autentifikácie medzi tabmi s refreshom stránky
authStore.syncAuthState();
</script>
