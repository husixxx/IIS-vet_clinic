<template>
  <div class="vet-requests-container">
    <h1>Veterinarian Requests</h1>

    <!-- Check if there are any requests -->
    <template v-if="requests.length > 0">
      <DataTable :value="requests" class="p-datatable-striped">
        <Column field="id" header="ID"></Column>
        <Column field="animal_id" header="Animal ID"></Column>
        <Column field="start_time" header="Start Time"></Column>
        <Column field="description" header="Description"></Column>
        <Column field="status" header="Status">
          <template #body="slotProps">
            <span>{{ typeof slotProps.data.status === 'string' ? slotProps.data.status : slotProps.data.status.value }}</span>
          </template>
        </Column>
        <Column header="Actions">
          <template #body="slotProps">
            <Button label="Edit" icon="pi pi-pencil" class="p-button-text p-button-sm" @click="openEditModal(slotProps.data)" />
          </template>
        </Column>
      </DataTable>
    </template>

    <!-- Display a message when no requests are found -->
    <template v-else>
      <div class="no-requests-message">
        No requests available for this veterinarian.
      </div>
    </template>

    <!-- Dialog (pop-up) for editing request status and start time -->
    <Dialog v-model:visible="editDialogVisible" header="Edit Request" class="centered-header">
      <div class="p-fluid">
        <!-- Edit Start Time -->
        <div class="p-field">
          <InputText v-model="selectedRequest.start_time" 
          :invalid="!selectedRequest.start_time"
          placeholder="DD/MM/YYYY, HH:MM:SS"/>
        </div>

        <!-- Edit Status -->
        <Dropdown
          v-model="selectedRequest.newStatus"
          :options="statusOptions"
          optionLabel="label"
          placeholder="Select Status"
          class="w-full"
          :invalid="!selectedRequest.newStatus"
        />
      </div>
      <template #footer>
        <div class="dialog-footer">
          <Button label="Cancel" class="p-button-text" @click="cancelEdit" />
          <!-- Disable Save button if start_time or newStatus is empty -->
          <Button label="Save" class="p-button-primary" @click="saveRequestChanges" 
            :disabled="!selectedRequest.start_time || !selectedRequest.newStatus || !selectedRequest.newStatus.value" />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../store/Authstore'; // Assuming you have a Pinia store for user authentication
import axiosClient from '../api/api';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';

// Access the authenticated user's data
const authStore = useAuthStore();

// Array to store veterinarian requests
const requests = ref([]);

// Status options for the dropdown
const statusOptions = [
  { label: 'pending', value: 'pending' },
  { label: 'scheduled', value: 'scheduled' },
  { label: 'cancelled', value: 'cancelled' },
  { label: 'completed', value: 'completed' }
];

// State to control the edit dialog visibility
const editDialogVisible = ref(false);

// Currently selected request for editing
const selectedRequest = ref(null);

// Fetch requests when the component mounts
onMounted(async () => {
  try {
    // Get the veterinarian's ID from the authenticated user
    const vetId = authStore.getUser?.id;

    // Make an API request to get requests by vet_id
    const response = await axiosClient.get(`/veterinarian/get_all_requests_by_vet_id`, {
      params: {
        vet_id: vetId,
      },
      withCredentials: true
    });

    if (response.data) {
      requests.value = response.data.map((request) => ({
        id: request.id,
        animal_id: request.animal_id,
        vet_id: request.vet_id,
        start_time: new Date(request.start_time).toLocaleString(),
        description: request.description,
        status: request.status || 'N/A',
        newStatus: request.status,
      }));
    }
  } catch (error) {
    console.error('Error fetching veterinarian requests:', error);
  }
});

const openEditModal = async (request) => {
  selectedRequest.value = { ...request }; // Clone the request
  selectedRequest.value.newStatus = null; // Nastav status na prázdne pole
  editDialogVisible.value = true;
};

// Cancel editing
const cancelEdit = async () => {
  selectedRequest.value = null;
  editDialogVisible.value = false;
};

// Save the updated request (start time and status)
const saveRequestChanges = async () => {
  try {
    // Convert from 'MM/DD/YYYY, HH:MM:SS' (which is what .toLocaleString() gives) to 'YYYY-MM-DD HH:MM:SS'
    const [datePart, timePart] = selectedRequest.value.start_time.split(', '); // Separate date and time

    const [month, day, year] = datePart.split('/'); // Split the MM/DD/YYYY part
    // Correct the order to format as 'YYYY-MM-DD HH:MM:SS'
    const formattedDateTime = `${year}-${day.padStart(2, '0')}-${month.padStart(2, '0')} ${timePart}`; // Corrected the order of month and day


    // Make the request to the backend with the properly formatted date and status
    const response = await axiosClient.post(`/veterinarian/schedule_request`, null, {
      params: {
        request_id: selectedRequest.value.id,
        date_time: formattedDateTime, // Send as 'YYYY-MM-DD HH:MM:SS'
        status: selectedRequest.value.newStatus.value,
      },
      withCredentials: true
    });

    if (response.status === 200) {
      const index = requests.value.findIndex((req) => req.id === selectedRequest.value.id);
      requests.value[index].status = selectedRequest.value.newStatus;
      requests.value[index].start_time = selectedRequest.value.start_time;
      editDialogVisible.value = false;
      selectedRequest.value = null;
    } else {
      console.error('Failed to update request');
    }
  } catch (error) {

    
    console.error('Error: Invalid date format ', error);
    alert('Error: Invalid date format ', error);

    
  }
};
</script>

<style scoped>
.vet-requests-container {
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

.p-button-sm {
  margin-left: 10px;
}

.p-dialog .p-fluid {
  padding: 20px;
}

.w-full {
  width: 100%;
}

/* Center the header text in the dialog */
.centered-header .p-dialog-titlebar {
  text-align: center;
  justify-content: center;
}

/* Center buttons in the footer */
.dialog-footer {
  display: flex;
  justify-content: center;
}

/* Red border for invalid fields */
.invalid-field {
  border-color: red !important;
}
</style>
