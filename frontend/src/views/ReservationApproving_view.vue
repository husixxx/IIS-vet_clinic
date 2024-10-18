<template>
    <div class="reservations-container">
      <h1>All Reservations</h1>
      <DataTable :value="reservations" class="p-datatable-striped">
        <Column field="id" header="ID"></Column>
        <Column field="animal_name" header="Animal"></Column>
        <Column field="volunteer_name" header="Volunteer"></Column>
        <Column field="start_time" header="Start Time"></Column>
        <Column field="end_time" header="End Time"></Column>
        <Column field="status" header="Status"></Column>
      </DataTable>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axiosClient from '../api/api';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  
  const reservations = ref([]);
  
  // Fetch reservations on component mount
  onMounted(async () => {
    try {
      const response = await axiosClient.get('/caretaker/get_all_reservations');
      if (response.data.reservations) {
        reservations.value = response.data.reservations.map(res => ({
          id: res.id,
          animal_name: res.animal.name,
          volunteer_name: res.volunteer.name,
          start_time: new Date(res.start_time).toLocaleString(),
          end_time: new Date(res.end_time).toLocaleString(),
          status: res.status
        }));
      }
    } catch (error) {
      console.error('Error fetching reservations:', error);
    }
  });
  </script>
  
  <style scoped>
  .reservations-container {
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
  </style>
  