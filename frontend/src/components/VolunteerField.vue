<template>
  <div class="volunteer-approval-container">
    <h1>Volunteer Approval</h1>
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
    const response = await axiosClient.get('/caretaker/unverified_volunteers', { withCredentials: true });
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
    const response = await axiosClient.post(`/caretaker/verify_volunteer?id=${volunteer.id}`, null, {
      withCredentials: true // Ensure cookies are sent and received
    });

    if (response.data.verified) {
      // Notify the user about the successful verification
      alert(`Volunteer ${volunteer.name} was verified successfully.`);
      // Reload the page to fetch updated data
      location.reload();
    }
  } catch (error) {
    if (error.response) {
      const status = error.response.status;
      const error_msg = error.response.data.error;
      console.error(`Error Status: ${status}`);
      alert(error_msg);
    } else {
      console.error("Error:", error.message);
      alert("Something went wrong. Please try again later.");
    }
  }
};
</script>

<style scoped>
.volunteer-approval-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  margin-bottom: 100px;
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
