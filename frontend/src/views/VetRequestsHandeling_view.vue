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
            <!-- Show edit button only for statuses 'pending' and 'scheduled' -->
            <Button
              v-if="['pending', 'scheduled'].includes(slotProps.data.status)"
              label="Edit"
              icon="pi pi-pencil"
              class="p-button-text p-button-sm"
              @click="openEditModal(slotProps.data)"
            />
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
          <InputText
            v-model="selectedRequest.start_time"
            maxlength="19"
            placeholder="DD/MM/YYYY HH:MM:SS"
            class="input-full-width"
            :class="{ 'p-invalid': !selectedRequest.start_time }"
          />
        </div>

        <!-- Edit Status -->
        <div class="p-field">
          <!-- Dropdown for status change -->
          <Dropdown
            v-model="selectedRequest.newStatus"
            :options="availableStatusOptions"
            optionLabel="label"
            placeholder="Select Status"
            class="input-full-width"
            :disabled="!availableStatusOptions.length"
          />
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <Button label="Cancel" class="p-button-text" @click="cancelEdit" />
          <Button label="Save" class="p-button-primary" :disabled="!isFormValid" @click="saveRequestChanges" />
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '../store/Authstore';
import axiosClient from '../api/api';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import Dropdown from 'primevue/dropdown';
import InputText from 'primevue/inputtext';

// Status options mapping
const statusOptionsMapping = {
  pending: [
    { label: 'scheduled', value: 'scheduled' },
    { label: 'cancelled', value: 'cancelled' },
  ],
  scheduled: [
    { label: 'completed', value: 'completed' },
    { label: 'cancelled', value: 'cancelled' },
  ],
  cancelled: [], // No actions available
  completed: [], // No actions available
};

// Convert custom date to standard format
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

  const [weekday, day, month, year, time] = customDateTime.split(' ');
  const formattedDate = `${day}/${months[month]}/${year} ${time}`;
  return formattedDate;
};

// Form validation
const isFormValid = computed(() => {
  return selectedRequest.value.start_time && selectedRequest.value.newStatus?.value;
});

const authStore = useAuthStore();
const requests = ref([]);
const editDialogVisible = ref(false);
const selectedRequest = ref({ start_time: '', newStatus: null });
const availableStatusOptions = ref([]);

// Validate datetime format
const isValidDateTime = (dateTimeStr) => {
  const regex = /^\d{2}\/\d{2}\/\d{4} \d{2}:\d{2}:\d{2}$/;
  return regex.test(dateTimeStr);
};

// Fetch requests
onMounted(async () => {
  try {
    const vetId = authStore.getUser?.id;
    const response = await axiosClient.get('/veterinarian/get_all_requests_by_vet_id', {
      params: { vet_id: vetId },
      withCredentials: true,
    });

    if (response.data) {
      requests.value = response.data.map((request) => ({
        id: request.id,
        animal_id: request.animal_id,
        animal_name: request.animal_name,
        vet_id: request.vet_id,
        start_time: request.start_time,
        description: request.description,
        status: request.status || 'N/A',
        newStatus: request.status,
      }));
    }
  } catch (error) {
    console.error('Error fetching veterinarian requests:', error);
  }
});

// Open edit modal
const openEditModal = (request) => {
  if (['cancelled', 'completed'].includes(request.status)) {
    alert('Requests with status "cancelled" or "completed" cannot be edited.');
    return;
  }

  selectedRequest.value = {
    ...request,
    start_time: convertCustomToStandard(request.start_time),
    newStatus: request.status,
  };

  availableStatusOptions.value = statusOptionsMapping[request.status] || [];
  editDialogVisible.value = true;
};

// Cancel editing
const cancelEdit = () => {
  selectedRequest.value = null;
  editDialogVisible.value = false;
};

// Convert date to backend format
const convertToBackendFormat = (frontendDateTime) => {
  const [datePart, timePart] = frontendDateTime.split(' ');
  const [day, month, year] = datePart.split('/');
  return `${year}-${month}-${day} ${timePart}`;
};

// Save changes
const saveRequestChanges = async () => {
  try {
    if (!isValidDateTime(selectedRequest.value.start_time)) {
      alert('Invalid date format. Use DD/MM/YYYY HH:MM:SS.');
      return;
    }

    const convertedDateTime = convertToBackendFormat(selectedRequest.value.start_time);

    const response = await axiosClient.post('/veterinarian/schedule_request', null, {
      params: {
        request_id: selectedRequest.value.id,
        date_time: convertedDateTime,
        status: selectedRequest.value.newStatus.value,
      },
      withCredentials: true,
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

.p-field {
  margin-bottom: 1rem;
}

.input-full-width {
  width: 100%;
}

.p-dialog {
  width: 400px;
  max-width: 90%;
}
</style>
