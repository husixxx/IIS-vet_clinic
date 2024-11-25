<template>
  <div class="caretaker-vet-requests-container">
    <h1>Caretaker Vet Requests</h1>

    <!-- Check if there are any requests -->
    <template v-if="requests.length > 0">
      <DataTable :value="requests" class="p-datatable-striped">
        <Column field="id" header="ID"></Column>
        <Column field="animal_id" header="Animal ID"></Column>
        <Column field="animal_name" header="Animal Name"></Column> <!-- Added Animal Name -->
        <Column field="request_date" header="Request Date"></Column>
        <Column field="description" header="Description"></Column>
        <Column field="status" header="Status">
          <template #body="slotProps">
            <span>{{ typeof slotProps.data.status === 'string' ? slotProps.data.status : slotProps.data.status.value }}</span>
          </template>
        </Column>
        <Column field="veterinarian_username" header="Veterinarian Username"></Column>
        <Column header="Actions">
          <template #body="slotProps">
            <Button
              v-if="slotProps.data.status === 'pending' || slotProps.data.status === 'scheduled'"
              label="Cancel"
              icon="pi pi-times"
              class="p-button-danger"
              @click="cancelVetRequest(slotProps.data.id)"
            />
          </template>
        </Column>
      </DataTable>
    </template>

    <!-- Display a message when no requests are found -->
    <template v-else>
      <div class="no-requests-message">
        No vet requests found.
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axiosClient from '../api/api';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';

// Array to store caretaker vet requests
const requests = ref([]);

// Helper function to format the date in UTC
const formatDateToUTC = (dateStr) => {
  const date = new Date(dateStr); // Parse the date string
  const year = date.getUTCFullYear();
  const month = String(date.getUTCMonth() + 1).padStart(2, '0'); // Months are zero-indexed
  const day = String(date.getUTCDate()).padStart(2, '0');
  const hours = String(date.getUTCHours()).padStart(2, '0');
  const minutes = String(date.getUTCMinutes()).padStart(2, '0');
  const seconds = String(date.getUTCSeconds()).padStart(2, '0');
  return `${day}/${month}/${year}, ${hours}:${minutes}:${seconds}`; // Format in DD/MM/YYYY, HH:MM:SS
};

// Fetch requests when the component mounts
onMounted(async () => {
  try {
    // Make an API request to get all vet requests for caretakers
    const response = await axiosClient.get('/caretaker/get_all_vet_requests', { withCredentials: true });

    if (response.data) {
      requests.value = response.data.map((request) => ({
        id: request.id,
        animal_id: request.animal_id,
        animal_name: request.animal_name, // Include Animal Name
        request_date: formatDateToUTC(request.request_date), // Convert date to UTC format
        description: request.description,
        status: request.status || 'N/A',
        veterinarian_username: request.veterinarian_username,
      }));
    }
  } catch (error) {
    console.error('Error fetching caretaker vet requests:', error);
  }
});

// Function to cancel a vet request
const cancelVetRequest = async (vetRequestId) => {
  try {
    const response = await axiosClient.delete('/caretaker/cancel_vet_request', {
      params: {
        vet_request_id: vetRequestId,
      },
      withCredentials: true
    });

    if (response.status === 200) {
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
.caretaker-vet-requests-container {
  padding: 20px;
  margin-bottom: 100px;
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
