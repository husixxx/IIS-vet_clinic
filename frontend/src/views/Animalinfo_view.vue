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

    <div class="medical-records-section">
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
                    v-if="user.id === slotProps.data.veterinarian_id"
                    label="Edit record"
                    @click="openMedicalRecordEditModal(slotProps.data)"
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

  <EditDialog
    :header="'Edit schedule'"
    :isVisible="showScheduleEditDialog"
    :fields="reservSchedulesFields"
    :model="selectedSchedule"
    :onSave="updateSchedule"
    :onCancel="closeScheduleEditModal"
  />

  <EditDialog
    :header="'Edit medical record'"
    :isVisible="showMedicalRecordsEditDialog"
    :fields="medicalRecordsFields"
    :model="selectedMedicalRecord"
    :onSave="updateMedicalRecord"
    :onCancel="closeMedicalRecordEditModal"
  />

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
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import { getFormattedDate } from '../utils/date';
import 'primeicons/primeicons.css'
import EditDialog from '../components/EditDialog.vue';

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
  startDateAnotherFormat: '',
  endDateAnotherFormat: '',
  startDate: '',
  endDate: '',
});

const showMedicalRecordsEditDialog = ref(false);
const selectedMedicalRecord = reactive({
  id: null,
  description: '',
  examinationDate: '',
  examinationType: ''
});

const reservSchedulesFields = [
  { 
    id: 'startDate',
    label: 'Start date',
    model: 'startDate',
    component: DatePicker,
    props: 
    {
      dateFormat: "yy-mm-dd",
      showTime: true,
      showSeconds: true,
      hourFormat: '24',
      manualInput: false,
      showIcon: true,
      iconDisplay: "input"
    }
  },
  { 
    id: 'endtDate',
    label: 'End date ',
    model: 'endDate',
    component: DatePicker,
    props: 
    {
      dateFormat: "yy-mm-dd",
      showTime: true,
      showSeconds: true,
      hourFormat: '24',
      manualInput: false,
      showIcon: true,
      iconDisplay: "input"
    }
  }
];

const medicalRecordsFields = [
  { 
    id: 'description',
    label: 'Description',
    model: 'description',
    component: Textarea,
    // props: 
    // {
    //   // model: 'scheduleStartTime',
    // }
  },
  {
    id: 'examinationDate',
    label: 'Examination date',
    model: 'examinationDate',
    component: DatePicker,
    props: 
    {
      dateFormat: "yy-mm-dd",
      showTime: true,
      showSeconds: true,
      hourFormat: '24',
      manualInput: false,
      showIcon: true,
      iconDisplay: "input"
    }
  },
  {
    id: 'examinationType',
    label: 'Examination type',
    model: 'examinationType',
    component: InputText
  }
];

const updateSchedule = async () => {
  try {
    console.log(`/caretaker/update_walking_schedule?walking_schedule_id=${encodeURIComponent(selectedSchedule.id)}` +
                                           `&start_time=${encodeURIComponent(getFormattedDate(selectedSchedule.startDate, true))}` +
                                           `&end_time=${encodeURIComponent(getFormattedDate(selectedSchedule.endDate, true))}`);
    console.log(`/caretaker/update_walking_schedule?walking_schedule_id=${selectedSchedule.id}` +
                                           `&start_time=${getFormattedDate(selectedSchedule.startDate, true)}` +
                                           `&end_time=${getFormattedDate(selectedSchedule.endDate, true)}`);
    const response = await axiosClient.put(`/caretaker/update_walking_schedule?walking_schedule_id=${encodeURIComponent(selectedSchedule.id)}` +
                                           `&start_time=${encodeURIComponent(getFormattedDate(selectedSchedule.startDate, true))}` +
                                           `&end_time=${encodeURIComponent(getFormattedDate(selectedSchedule.endDate, true))}`);
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

const updateMedicalRecord = async () => {
  try {
    console.log(`/caretaker/update_medical_record?medical_record_id=${selectedMedicalRecord.id}` +
                                           `&veterinarian_id=${authStore.getUser.id}` +
                                           `&examination_date=${getFormattedDate(selectedMedicalRecord.examinationDate)}` +
                                           `&examination_type=${selectedMedicalRecord.examinationType}` +
                                           `&description=${selectedMedicalRecord.description}`);
    console.log(`/caretaker/update_medical_record?medical_record_id=${encodeURIComponent(selectedMedicalRecord.id)}` +
                                           `&veterinarian_id=${encodeURIComponent(authStore.getUser.id)}` +
                                           `&examination_date=${encodeURIComponent(getFormattedDate(selectedMedicalRecord.examinationDate))}` +
                                           `&examination_type=${encodeURIComponent(selectedMedicalRecord.examinationType)}` +
                                           `&description=${encodeURIComponent(selectedMedicalRecord.description)}`);
    const response = await axiosClient.put(`/caretaker/update_medical_record?medical_record_id=${encodeURIComponent(selectedMedicalRecord.id)}` +
                                           `&veterinarian_id=${encodeURIComponent(authStore.getUser.id)}` +
                                           `&examination_date=${encodeURIComponent(getFormattedDate(selectedMedicalRecord.examinationDate))}` +
                                           `&examination_type=${encodeURIComponent(selectedMedicalRecord.examinationType)}` +
                                           `&description=${encodeURIComponent(selectedMedicalRecord.description)}`);
    if(response.status === 200) {
      alert('Medical record updated successfully!');
      closeMedicalRecordEditModal();
      onMounted();
    }
  } catch (error) {
    console.error('Error updating medical record:', error);
    alert('Failed to update medical record.');
  }
};


const openScheduleEditModal = async (schedule) => {
  selectedSchedule.startDateAnotherFormat = schedule.start_time;
  selectedSchedule.endDateAnotherFormat = schedule.end_time;
  selectedSchedule.startDate = getFormattedDate(selectedSchedule.startDateAnotherFormat, true);
  selectedSchedule.endDate = getFormattedDate(selectedSchedule.endDateAnotherFormat, true);
  selectedSchedule.id = schedule.id;
  // console.log('Mounted: ', schedule);
  showScheduleEditDialog.value = true;
};

const closeScheduleEditModal = async () => {
  showScheduleEditDialog.value = false;
};

const openMedicalRecordEditModal = async (medicalRecord) => {
  console.log('openMedicalRecordEditModal: ', medicalRecord);
  selectedMedicalRecord.id = medicalRecord.id;
  selectedMedicalRecord.description = medicalRecord.description;
  selectedMedicalRecord.examinationDate = medicalRecord.examination_date;
  selectedMedicalRecord.examinationType = medicalRecord.examination_type;
  // console.log('Mounted: ', selectedSchedule);
  showMedicalRecordsEditDialog.value = true;
};

const closeMedicalRecordEditModal = async () => {
  showMedicalRecordsEditDialog.value = false;
};


onMounted(async () => {
  try {
    const response = await axiosClient.get(`/animal/info?animal_id=${encodeURIComponent(route.params.id)}`);
    // console.log(response.data);
    animalInfo.value = response.data;
    animalSchedules.value = animalInfo.value.schedules;
    animalMedicalRecords.value = animalInfo.value.medical_records;
    console.log(animalMedicalRecords.value);
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

.medical-records-section {
  grid-column: 2 / span 1;
  grid-row: 2 / span 1;
}

.animal-schedules, .animal-info, .medical-records-section {
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
  