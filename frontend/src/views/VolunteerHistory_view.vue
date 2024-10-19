<template>
    <div class="volunteer-history-container">
      <h1>Volunteer History</h1>
  
      <!-- Check if there are any reservations -->
      <template v-if="reservations.length > 0">
        <DataTable :value="reservations" class="p-datatable-striped">
          <Column field="id" header="Reservation ID"></Column>
          <Column field="animal_id" header="Animal ID"></Column>
          <Column field="volunteer_username" header="Volunteer Username"></Column>
          <Column field="start_time" header="Start Time"></Column>
          <Column field="end_time" header="End Time"></Column>
          <Column field="status" header="Status">
            <template #body="slotProps">
              <span>{{ typeof slotProps.data.status === 'string' ? slotProps.data.status : slotProps.data.status.value }}</span>
            </template>
          </Column>
        </DataTable>
      </template>
  
      <!-- Display a message when no reservations are found -->
      <template v-else>
        <div class="no-history-message">
          No reservation history available for this volunteer.
        </div>
      </template>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useAuthStore } from '../store/Authstore'; // Assuming you have a Pinia store for user authentication
  import axiosClient from '../api/api';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  
  // Access the authenticated user's data (volunteer)
  const authStore = useAuthStore();
  
  // Array to store volunteer's reservation history
  const reservations = ref([]);
  
  // Fetch reservations when the component mounts
  onMounted(async () => {
    try {
      // Get the volunteer's ID from the authenticated user
      const volunteerId = authStore.getUser?.id;

      console.log(volunteerId);
  
      // Make an API request to get reservations by volunteer_id
      const response = await axiosClient.get('/volunteer/get_reservations_by_volunteer_id', {
        params: {
          volunteer_id: volunteerId,
        },
      });
  
      if (response.data) {
        reservations.value = response.data.map((reservation) => ({
          id: reservation.id,
          animal_id: reservation.animal_id,
          volunteer_username: reservation.volunteer_username,
          start_time: new Date(reservation.start_time).toLocaleString(),
          end_time: new Date(reservation.end_time).toLocaleString(),
          status: reservation.status || 'N/A',
        }));
      }
    } catch (error) {
      console.error('Error fetching reservation history:', error);
    }
  });
  </script>
  
  <style scoped>
  .volunteer-history-container {
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
  
  .no-history-message {
    text-align: center;
    font-size: 1.2rem;
    color: #777;
    padding: 40px;
  }
  </style>
  