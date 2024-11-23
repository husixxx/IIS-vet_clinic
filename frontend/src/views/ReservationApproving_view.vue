<template>
  <div class="reservations-container">
    <h1>All Reservations</h1>

    <!-- Check if there are reservations -->
    <template v-if="reservations.length > 0">
      <DataTable :value="reservations" class="p-datatable-striped">
        <Column field="id" header="ID"></Column>
        <Column field="animal_id" header="Animal ID"></Column>
        <Column field="animal_name" header="Animal Name"></Column>
        <Column field="volunteer_username" header="Volunteer Username"></Column>
        <Column field="start_time" header="Start Time"></Column>
        <Column field="end_time" header="End Time"></Column>
        <Column header="Status">
          <template #body="slotProps">
            <div>
              <!-- Display the current status -->
              <span>{{ typeof slotProps.data.status === 'string' ? slotProps.data.status : slotProps.data.status.value }}</span>
              <!-- Show edit button based on status -->
              <Button
                v-if="canEditStatus(slotProps.data.status)"
                label="Edit"
                icon="pi pi-pencil"
                class="p-button-text p-button-sm"
                @click="openEditModal(slotProps.data)"
              />
            </div>
          </template>
        </Column>
      </DataTable>
    </template>

    <!-- Display a message when there are no reservations -->
    <template v-else>
      <div class="no-reservations-message">
        No reservations waiting for approval.
      </div>
    </template>

    <!-- Dialog (pop-up) for editing status -->
    <Dialog v-model:visible="editDialogVisible" header="Edit Reservation Status">
      <div class="p-fluid">
        <Dropdown
          v-model="selectedReservation.newStatus"
          :options="getStatusOptions(selectedReservation?.status)"
          optionLabel="label"
          placeholder="Select Status"
          class="w-full"
          :invalid="!selectedReservation.newStatus"
        />
      </div>
      <template #footer>
        <Button label="Cancel" class="p-button-text" @click="cancelEdit" />
        <Button
          label="Save"
          class="p-button-primary"
          @click="saveStatus"
          :disabled="!selectedReservation.newStatus"
        />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axiosClient from '../api/api';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';

// Array to store reservations
const reservations = ref([]);

// Status options for the dropdown
const allStatusOptions = {
  pending: [
    { label: 'approved', value: 'approved' },
    { label: 'cancelled', value: 'cancelled' }
  ],
  approved: [
    { label: 'completed', value: 'completed' }
  ]
};

// State to control the edit dialog visibility
const editDialogVisible = ref(false);

// Currently selected reservation for editing
const selectedReservation = ref(null);

// Fetch reservations when the component mounts
onMounted(async () => {
  try {
    const response = await axiosClient.get('/caretaker/get_all_reservations', {
      withCredentials: true // Ensure cookies are sent and received
    });

    if (response.data) {
      reservations.value = response.data.map(reservation => ({
        id: reservation.id, // Now using the correct reservation id
        animal_id: reservation.animal_id,
        animal_name: reservation.animal_name, // Include Animal Name
        volunteer_username: reservation.volunteer_username, // Update volunteer ID to username
        start_time: new Date(reservation.start_time).toLocaleString(),
        end_time: new Date(reservation.end_time).toLocaleString(),
        status: reservation.status || 'N/A', // Initial status from DB
        newStatus: reservation.status // Store the initial status
      }));
    }
  } catch (error) {
    console.error('Error fetching reservations:', error);
  }
});

// Get dropdown options based on current status
const getStatusOptions = (status) => {
  return allStatusOptions[status] || [];
};

// Check if the reservation's status can be edited
const canEditStatus = (status) => {
  return status === 'pending' || status === 'approved';
};

// Open the edit modal
const openEditModal = (reservation) => {
  selectedReservation.value = { ...reservation }; // Clone the reservation
  selectedReservation.value.newStatus = null;
  editDialogVisible.value = true;
};

// Cancel editing
const cancelEdit = () => {
  selectedReservation.value = null;
  editDialogVisible.value = false;
};

// Save the new status
const saveStatus = async () => {
  try {
    const response = await axiosClient.post('/caretaker/change_reservation_status', null, {
      params: {
        id: selectedReservation.value.id,
        status: selectedReservation.value.newStatus.value
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
      console.error('Error:', error.message);
      alert('Something went wrong. Please try again later.');
    }
  }
};
</script>

<style scoped>
.reservations-container {
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

.no-reservations-message {
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
</style>
