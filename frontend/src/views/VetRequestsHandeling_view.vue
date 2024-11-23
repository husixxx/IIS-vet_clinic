<template>
  <div class="vet-requests-container">
    <h1>Veterinarian Requests</h1>

    <!-- Check if there are any requests -->
    <template v-if="requests.length > 0">
      <DataTable :value="requests" class="p-datatable-striped">
        <Column field="id" header="ID"></Column>
        <Column field="animal_id" header="Animal ID"></Column>
        <Column field="animal_name" header="Animal Name"></Column>
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
                     maxlength="19"
                     placeholder="DD/MM/YYYY HH:MM:SS"/>
        </div>

        <!-- Edit Status -->
        <Dropdown
          v-model="selectedRequest.newStatus"
          :options="statusOptions"
          optionLabel="label"
          placeholder="Select Status"
          class="w-full"
        />
      </div>
      <template #footer>
        <div class="dialog-footer">
          <Button label="Cancel" class="p-button-text" @click="cancelEdit" />
          <Button label="Save" class="p-button-primary" @click="saveRequestChanges" />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../store/Authstore';
import axiosClient from '../api/api';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';

const convertCustomToStandard = (customDateTime) => {
  const months = {
    Jan: '01',
    Feb: '02',
    Mar: '03',
    Apr: '04',
    May: '05',
    Jun: '06',
    Jul: '07',
    Aug: '08',
    Sep: '09',
    Oct: '10',
    Nov: '11',
    Dec: '12',
  };

  const [weekday, day, month, year, time] = customDateTime.split(' '); // Rozdelenie stringu
  const formattedDate = `${day}/${months[month]}/${year} ${time}`; // Formátovanie na DD/MM/YYYY HH:MM:SS
  return formattedDate;
};

// Access the authenticated user's data
const authStore = useAuthStore();
const requests = ref([]);
const statusOptions = [
  { label: 'pending', value: 'pending' },
  { label: 'scheduled', value: 'scheduled' },
  { label: 'cancelled', value: 'cancelled' },
  { label: 'completed', value: 'completed' },
];
const editDialogVisible = ref(false);
const selectedRequest = ref({ start_time: '', newStatus: null });

// Validate the string format of the date
const isValidDateTime = (dateTimeStr) => {
  const regex = /^\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}:\d{2}$/;
  return regex.test(dateTimeStr);
};

// Fetch requests when the component mounts
onMounted(async () => {
  try {
    const vetId = authStore.getUser?.id;

    const response = await axiosClient.get(`/veterinarian/get_all_requests_by_vet_id`, {
      params: { vet_id: vetId },
      withCredentials: true,
    });

    if (response.data) {
      requests.value = response.data.map((request) => ({
        id: request.id,
        animal_id: request.animal_id,
        animal_name: request.animal_name,
        vet_id: request.vet_id,
        start_time: request.start_time, // Store as string directly
        description: request.description,
        status: request.status || 'N/A',
        newStatus: request.status,
      }));
    }
  } catch (error) {
    console.error('Error fetching veterinarian requests:', error);
  }
});

const openEditModal = (request) => {
  selectedRequest.value = {
    ...request,
    start_time: convertCustomToStandard(request.start_time), // Konverzia na DD/MM/YYYY HH:MM:SS
    newStatus: request.status,
  };
  editDialogVisible.value = true;
};

const cancelEdit = () => {
  selectedRequest.value = null;
  editDialogVisible.value = false;
};

const convertToBackendFormat = (frontendDateTime) => {
  const [datePart, timePart] = frontendDateTime.split(' ');
  const [day, month, year] = datePart.split('/');
  return `${year}-${month}-${day} ${timePart}`; // Convert to 'YYYY-MM-DD HH:MM:SS'
};

const saveRequestChanges = async () => {
  try {
    if (!isValidDateTime(selectedRequest.value.start_time)) {
      alert('Invalid date format. Use DD/MM/YYYY HH:MM:SS.');
      return;
    }

    const converstion = convertToBackendFormat(selectedRequest.value.start_time);

    const response = await axiosClient.post(`/veterinarian/schedule_request`, null, {
      params: {
        request_id: selectedRequest.value.id,
        date_time: converstion, // Send as string
        status: selectedRequest.value.newStatus.value,
      },
      withCredentials: true,
    });

    if (response.status === 200) {
      const index = requests.value.findIndex((req) => req.id === selectedRequest.value.id);
      requests.value[index].status = selectedRequest.value.newStatus;
      requests.value[index].start_time = selectedRequest.value.start_time;
      editDialogVisible.value = false;
      selectedRequest.value = null;
    }
  } catch (error) {
    console.error('Error updating request:', error);
    alert('Error updating request.');
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

.p-dialog .p-fluid {
  padding: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: center;
}

.invalid-field {
  border-color: red !important;
}
</style>
