<template>
  <div class="main-content">
    <!-- Div for the photo -->
    <div class="photo-section">
      <img src="../assets/cat3.jpg" alt="Animal photo" />
    </div>

      <!-- Div pre popis (description) -->
    <div class="animal-schedules">
      <h3 style="text-align: center;">Avaliable schedules</h3>
      <Button v-if="authStore.getRoleId === UserRole.Caretaker" label="Add schedule" class="p-button-warning" style="width: 100%;"/>
      <Card class="full-width-card">
        <template #content>
          <div class="p-fluid">
            <DataTable :value="animalSchedules" class="full-width-table" tableStyle="width: 100%">
              <Column field="start_time" header="Start date" style="width: 10%;"></Column>
              <Column field="end_time" header="End date" style="width: 10%;"></Column>
              <Column v-if="authStore.getRoleId === UserRole.Volunteer" header="" style="width: 5%; text-align: right;" headerStyle="text-align: right; padding-right: 30px;">
                <template #body="slotProps">
                  <Button
                    label="Make reservation"
                   
                    class="p-button-warning"
                  />
                </template>
              </Column>
              <Column v-if="authStore.getRoleId === UserRole.Caretaker" header="" style="width: 5%; text-align: right;" headerStyle="text-align: right; padding-right: 30px;">
                <template #body="slotProps">
                  <Button
                    label="Edit schedule"
                    @click="openScheduleEditModal(slotProps.data)"
                    class="p-button-warning"
                  />
                </template>
              </Column>
            </DataTable>
          </div>
        </template>
      </Card>
    </div>

    <!-- Medical records section -->
    <div class="animal-info">
      <!-- First column: Tags -->
      <div class="tags-column">
        <div class="tags">
          <strong>Name:</strong> {{ animalInfo?.animal?.name }}
        </div>
        <div class="tags">
          <strong>Age:</strong> {{ animalInfo?.animal?.age }}
        </div>
        <div class="tags">
          <strong>Breed:</strong> {{ animalInfo?.animal?.breed }}
        </div>
        <div class="tags">
          <strong>Sex:</strong> {{ animalInfo?.animal?.sex }}
        </div>
      </div>

      <!-- Second column: Fieldsets -->
      <div class="animal-fieldsets">
        <Fieldset legend="Description">
          <p>{{ animalInfo?.animal?.description }}</p>
        </Fieldset>
        <Fieldset legend="History">
          <p>{{ animalInfo?.animal?.history }}</p>
        </Fieldset>
      </div>
    </div>

    <!-- Schedule section -->
    <div class="medical-schedule-section">
      <h3 style="text-align: center;">Medical records</h3>
      <Button v-if="authStore.getRoleId === UserRole.Veterinarian" label="Add medical record" class="p-button-warning" style="width: 100%;"/>
      <Card class="full-width-card">
        <template #content>
          <div class="p-fluid">
            <DataTable :value="animalMedicalRecords" class="full-width-table" tableStyle="width: 100%">
              <Column field="description" header="Description" style="width: 45%;" bodyStyle="white-space: normal; word-break: break-word;"></Column>
              <Column field="examination_date" header="Examination date" style="width: 10%;"></Column>
              <Column field="examination_type" header="Examination type" style="width: 10%;"></Column>
              <Column v-if="authStore.getRoleId === UserRole.Veterinarian" header="" style="width: 10%; text-align: right;" headerStyle="text-align: right; padding-right: 30px;">
                <template #body="slotProps">
                  <Button
                    label="Edit record"
                   
                    class="p-button-warning"
                  />
                </template>
              </Column>
            </DataTable>
          </div>
        </template>
      </Card>
    </div>
  </div>

  <Dialog header="Edit schedule" v-model:visible="showScheduleEditDialog" :modal="true" :closable="true" :style="{ width: '50vw' }">
    <div class="p-fluid">
      <div class="p-field" v-for="field in reservSchedulesFields" :key="field.id">
        <label :for="field.id" class="input-label">{{ field.label }}</label>
        <component
          :is="field.component"
          v-model="selectedSchedule[field.model]"
          v-bind="field.props"
          :id="field.id"
          class="input-field"
        />
      </div>
    </div>
    <template #footer>
      <Button label="Save" @click="updateSchedule" class="p-button-success" />
      <Button label="Cancel" @click="closeScheduleEditModal" class="p-button-secondary" />
    </template>
  </Dialog>

</template>
  
<script setup>

import { ref, reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axiosClient from '../api/api';
import { useAuthStore, UserRole } from '../store/Authstore';  // Ensure correct import of your AuthStore
import Fieldset from 'primevue/fieldset';
import DataTable from 'primevue/datatable';
import Card from 'primevue/card';
import Column from 'primevue/column';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import DatePicker from 'primevue/datepicker';

const route = useRoute();
const authStore = useAuthStore();
const user = authStore.getUser;
const userRole = authStore.getRoleId;
const animalInfo = ref();
const animalSchedules = ref([]);
const animalMedicalRecords = ref([]);

const showScheduleEditDialog = ref(false);
const selectedSchedule = reactive({
  id: null,
  // animalId: null,
  startDate: '',
  endDate: ''
});

const reservSchedulesFields = [
  { 
    id: 'startDate',
    label: 'Start date',
    model: 'startDate',
    component: DatePicker,
    props: 
    {
      // model: 'scheduleStartTime',
      dateFormat: "yy-mm-dd",
      showTime: true,
      showSeconds: true,
      hourFormat: '24'
    }
  },
  { 
    id: 'endtDate',
    label: 'End date ',
    model: 'endDate',
    component: DatePicker,
    props: 
    {
      // model: 'scheduleEndTime',
      dateFormat: "yy-mm-dd",
      showTime: true,
      showSeconds: true,
      hourFormat: '24'
    }
  }
];

function formatDate(inputDate) {
    const date = new Date(inputDate);

    const year = date.getUTCFullYear();
    const month = String(date.getUTCMonth() + 1).padStart(2, '0');
    const day = String(date.getUTCDate()).padStart(2, '0');
    const hours = String(date.getUTCHours()).padStart(2, '0');
    const minutes = String(date.getUTCMinutes()).padStart(2, '0');
    const seconds = String(date.getUTCSeconds()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

const updateSchedule = async () => {
  try {
    console.log(`/caretaker/update_walking_schedule?walking_schedule_id=${encodeURIComponent(selectedSchedule.id)}` +
                                           `&start_time=${encodeURIComponent(formatDate(selectedSchedule.startDate))}` +
                                           `&end_time=${encodeURIComponent(formatDate(selectedSchedule.endDate))}`);
    console.log(`/caretaker/update_walking_schedule?walking_schedule_id=${selectedSchedule.id}` +
                                           `&start_time=${formatDate(selectedSchedule.startDate)}` +
                                           `&end_time=${formatDate(selectedSchedule.endDate)}`);
    const response = await axiosClient.put(`/caretaker/update_walking_schedule?walking_schedule_id=${encodeURIComponent(selectedSchedule.id)}` +
                                           `&start_time=${encodeURIComponent(formatDate(selectedSchedule.startTime))}` +
                                           `&end_time=${encodeURIComponent(formatDate(selectedSchedule.endTime))}`);
    if (response.status === 200) {
      alert('Schedule updated successfully!');
      closeScheduleEditModal();
      onMounted();
    }
  } catch (error) {
    console.error('Error updating schedule:', error);
    alert('Failed to update schedule.');
  }
};

const openScheduleEditModal = async (schedule) => {
  selectedSchedule.startTime = schedule.start_time;
  selectedSchedule.endTime = schedule.end_time;
  selectedSchedule.id = schedule.id;
  // console.log('Mounted: ', selectedSchedule);
  showScheduleEditDialog.value = true;
};

const closeScheduleEditModal = async () => {
  showScheduleEditDialog.value = false;
};

onMounted(async () => {
  try {
    const response = await axiosClient.get(`/animal/info?animal_id=${encodeURIComponent(route.params.id)}`);
    // console.log(response.data);
    animalInfo.value = response.data;
    animalSchedules.value = animalInfo.value.schedules;
    animalMedicalRecords.value = animalInfo.value.medical_records;
    // console.log('schedules: ', animalSchedules.value);
  } catch (error) {
    console.error('Error fetching animal data:', error);
  }
});

</script>
  
<style scoped>

.animal-schedules {
  grid-row: 2 / span 1;
  justify-content: center;
  align-items: center;
  /* padding: 20px; */
  width: 100%;
  /* Set min-height to ensure space for content without cutting off the table */
  min-height: 5vh; 
}

.full-width-card {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.p-fluid {
  flex-grow: 1;
}

.full-width-table {
  width: 100%;
}

.main-content {
  display: grid;
  grid-template-columns: 0.8fr 2.5fr;
  gap: 20px;
  padding: 20px;
  padding-bottom: 110px;
}

/* Layout for medical records section with two columns */
.animal-info {
  display: grid;
  grid-template-columns: 0.2fr 1fr; /* Two equal-width columns */
  gap: 20px;
}

.tags-column {
  display: flex;
  flex-direction: column;
  gap: 10px; /* Spacing between the tags */
  padding-top: 8px;
}

.tags {
  margin-bottom: 5px;
}

.animal-fieldsets {
  display: flex;
  flex-direction: column;
  gap: 0px; /* Spacing between the fieldsets */
}

fieldset {
  width: 100%;
  max-width: 800px;
  /* margin-bottom: 20px; */
}

.photo-section img {
  width: 100%;
  height: auto;
  object-fit: cover;
  border-radius: 10px;
}

.medical-medical-schedule-section {
  grid-column: 2 / span 1;
  grid-row: 2 / span 1;
}

.animal-schedules, .animal-info, .medical-medical-schedule-section {
  /* background-color: #f0f0f0; */
  border-radius: 10px;
}

.full-width-table .p-column-title, .full-width-table td {
  white-space: normal;
  word-break: break-word;
}

.full-width-table td {
  max-width: 100%; /* Ensure cells don't stretch beyond available space */
  padding: 10px;
}

</style>
  