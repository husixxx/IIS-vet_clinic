<template>
  <div class="reservations-container">
    <h1>All Reservations</h1>

    <!-- Check if there are reservations -->
    <template v-if="reservations.length > 0">
      <DataTable :value="reservations" class="p-datatable-striped">
        <Column field="id" header="ID"></Column>
        <Column field="animal_id" header="Animal ID"></Column>
        <Column field="volunteer_username" header="Volunteer Username"></Column>
        <Column field="start_time" header="Start Time"></Column>
        <Column field="end_time" header="End Time"></Column>
        <Column header="Status">
          <template #body="slotProps">
            <div>
              <!-- Check if status is a string or an object -->
              <span>{{ typeof slotProps.data.status === 'string' ? slotProps.data.status : slotProps.data.status.value }}</span>
              <Button label="Edit" icon="pi pi-pencil" class="p-button-text p-button-sm" @click="openEditModal(slotProps.data)" />
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
          :options="statusOptions"
          optionLabel="label"
          placeholder="Select Status"
          class="w-full"
        />
      </div>
      <template #footer>
        <Button label="Cancel" class="p-button-text" @click="cancelEdit" />
        <Button label="Save" class="p-button-primary" @click="saveStatus" />
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
const statusOptions = [
  { label: 'pending', value: 'pending' },
  { label: 'approved', value: 'approved' },
  { label: 'canceled', value: 'canceled' },
  { label: 'completed', value: 'completed' }
];

// State to control the edit dialog visibility
const editDialogVisible = ref(false);

// Currently selected reservation for editing
const selectedReservation = ref(null);

// Fetch reservations when the component mounts
onMounted(async () => {
  try {
    const response = await axiosClient.get('/caretaker/get_all_reservations', {
      withCredentials: true  // Zabezpečí, že cookies budú odoslané a prijaté
    });

    if (response.data) {
      reservations.value = response.data.map(reservation => ({
        id: reservation.id,  // Now using the correct reservation id
        animal_id: reservation.animal_id,
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

// Open the edit modal
const openEditModal = async (reservation) => {
  selectedReservation.value = { ...reservation }; // Clone the reservation
  editDialogVisible.value = true;
};

// Cancel editing
const cancelEdit = async () => {
  selectedReservation.value = null;
  editDialogVisible.value = false;
};

// Save the new status
const saveStatus = async () => {
  try {
    const response = await axiosClient.post(`/caretaker/change_reservation_status`, null, {
      params: {
        id: selectedReservation.value.id,
        status: selectedReservation.value.newStatus.value
      },
      withCredentials: true
    });
    if (response.status === 200) {
      const index = reservations.value.findIndex(res => res.id === selectedReservation.value.id);
      reservations.value[index].status = selectedReservation.value.newStatus;
      editDialogVisible.value = false;
      selectedReservation.value = null;
    } else {
      console.error('Failed to update status');
    }
  } catch (error) {
    console.error('Error updating status:', error);
  }
};
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
