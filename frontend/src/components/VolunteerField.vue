<template>
    <div class="volunteer-approval-container">
      <h2>Volunteer Approval</h2>
      <div class="card">
        <!-- Check if there are any volunteers -->
        <template v-if="volunteers.length > 0">
          <DataTable :value="volunteers" tableStyle="min-width: 50rem">
            <Column field="id" header="ID"></Column>
            <Column field="name" header="Name"></Column>
            <Column field="email" header="Email"></Column>
            <Column header="Status">
              <template #body="slotProps">
                <span v-if="slotProps.data.role_id === 1">Verified</span>
                <span v-else-if="slotProps.data.role_id === 5">Unverified</span>
              </template>
            </Column>
            <Column header="Actions">
              <template #body="slotProps">
                <Button
                  v-if="slotProps.data.role_id === 5"
                  label="Verify"
                  @click="verifyVolunteer(slotProps.data)"
                  class="p-button-success"
                />
              </template>
            </Column>
          </DataTable>
        </template>
  
        <!-- Display a message when there are no volunteers -->
        <template v-else>
          <div class="no-volunteers-message">
            No volunteers waiting to be approved.
          </div>
        </template>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import Button from 'primevue/button'; // Import Button from PrimeVue
  import axiosClient from '../api/api';
  
  // Reactive reference to hold volunteer data
  const volunteers = ref([]);
  
  // Fetch volunteers on component mount
  onMounted(async () => {
    try {
      // Make a GET request to the Flask API to fetch unverified volunteers
      const response = await axiosClient.get('/caretaker/unverified_volunteers');
      // Populate the table with the response data
      volunteers.value = response.data;
    } catch (error) {
      console.error('Error fetching unverified volunteers:', error);
    }
  });
  
  // Function to verify a volunteer
  const verifyVolunteer = async (volunteer) => {
    try {
      // Call the updated verification endpoint with the correct query parameter 'id'
      const response = await axiosClient.post(`/caretaker/verify_volunteer?id=${volunteer.id}`);
  
      if (response.data.verified) {
        // Update the local role_id to 1 if verified successfully
        volunteer.role_id = 1;
        alert(`Volunteer ${volunteer.name} was verified successfully.`);
      }
    } catch (error) {
      console.error('Error verifying volunteer:', error);
      alert('Failed to verify the volunteer.');
    }
  };
  </script>
  
  <style scoped>
  .volunteer-approval-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
  }
  
  h2 {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 20px;
  }
  
  .card {
    width: 100%;
  }
  
  .no-volunteers-message {
    text-align: center;
    font-size: 1.2rem;
    color: #777;
    padding: 40px;
  }
  </style>
  