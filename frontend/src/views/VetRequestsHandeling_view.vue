<template>
    <div class="requests-container">
      <h1>All Requests for Veterinarian</h1>
  
      <!-- Check if there are requests -->
      <template v-if="requests.length > 0">
        <DataTable :value="requests" class="p-datatable-striped">
          <Column field="id" header="Request ID"></Column>
          <Column field="animal_id" header="Animal ID"></Column>
          <Column field="vet_id" header="Veterinarian ID"></Column>
          <Column field="start_time" header="Start Time"></Column>
          <Column field="end_time" header="End Time"></Column>
          <Column field="status" header="Status"></Column>
          <Column field="description" header="Description"></Column>
        </DataTable>
      </template>
  
      <!-- Display a message when there are no requests -->
      <template v-else>
        <div class="no-requests-message">
          No requests found for this veterinarian.
        </div>
      </template>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useAuthStore } from '@/stores/auth';  // Path to your Pinia store
  import axiosClient from '../api/api';  // Ensure correct path to your API client
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  
  // Pinia store for authenticated user
  const authStore = useAuthStore();
  
  // Reactive reference to store the requests
  const requests = ref([]);
  
  // Fetch requests when the component mounts, using the logged-in veterinarian's ID
  onMounted(async () => {
    if (authStore.isLoggedIn && authStore.getRoleId === 2) {  // Ensure it's a veterinarian
      try {
        const response = await axiosClient.get(`/veterinarian/get_all_requests_by_vet_id`, {
          params: { vet_id: authStore.getUser.id }  // Use the logged-in veterinarian's ID
        });
        requests.value = response.data;
      } catch (error) {
        console.error('Error fetching requests:', error);
      }
    } else {
      console.warn('User is not logged in or not a veterinarian.');
    }
  });
  </script>
  
  <style scoped>
  .requests-container {
    padding: 20px;
  }
  
  h1 {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .p-datatable {
    width: 100%;
    margin-top: 20px;
  }
  
  .no-requests-message {
    text-align: center;
    font-size: 1.2rem;
    color: #777;
    padding: 40px;
  }
  </style>
  