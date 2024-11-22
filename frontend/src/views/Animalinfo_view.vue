<template>
  <div class="main-content">
    <div class="photo-section">
      <img :src="animalPhoto" alt="Animal photo" />
    </div>

    <div class="animal-schedules">
      <h3 style="text-align: center;">Avaliable schedules</h3>
      <ConfirmDialog />
      <Button v-if="authStore.getRoleId === UserRole.Caretaker" label="Create schedule" style="width: 100%;" @click="openScheduleAddModal({ start_time: '', end_time: '' })"/>
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
                    @click="confirmReservation(animalInfo?.name, slotProps.data)"
                  />
                </template>
              </Column>
              <Column v-if="authStore.getRoleId === UserRole.Caretaker" header="" style="width: 5%; text-align: right;" headerStyle="text-align: right; padding-right: 30px;">
                <template #body="slotProps">
                  <Button
                    label="Edit schedule"
                    @click="openScheduleEditModal(slotProps.data)"
                  />
                </template>
              </Column>
            </DataTable>
          </div>
        </template>
      </Card>
    </div>

    <div class="animal-info">
      <div class="tags-column">
        <div class="tags non-prime-animal-info" v-for="(field, index) in filteredAnimalInfoFields" :key="index">
          <strong>{{ field.label }}:</strong> {{ animalInfo?.[field.model] }}
        </div>
        
        <div class="tags" v-if="authStore.getRoleId === UserRole.Caretaker">
          <Button label="Edit animal information" style="width: 100%;" @click="openAnimalInfoEditModal(animalInfo)"/>
        </div>
        <div class="tags" v-if="authStore.getRoleId === UserRole.Caretaker">
          <Button
            @click="() => router.push({ name: 'CreateVetRequest', params: { animalId: route.params.id } })"
            label="Create veterinarian request"
            style="width: 100%;"
          />
        </div>
        <div class="tags" v-if="authStore.getRoleId === UserRole.Caretaker">
          <Button
            @click="confirmAnimalDeletion()"
            label="Delete animal"
            style="width: 100%;"
            class="p-button-danger"
          />
        </div>
      </div>

      <div class="animal-fieldsets">
        <Fieldset legend="Description">
          <p>{{ animalInfo?.description }}</p>
        </Fieldset>
        <Fieldset legend="History">
          <p>{{ animalInfo?.history }}</p>
        </Fieldset>
      </div>
  </div>

    <div class="medical-records-section">
      <h3 style="text-align: center;">Medical records</h3>
      <Button v-if="authStore.getRoleId === UserRole.Veterinarian" label="Add medical record" class="p-button-warning" style="width: 100%;" @click="openMedicalRecordAddModal({ description: '', examinationDate: '', examinationType: '' })"/>
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

  <EditAddDialog
    header="Edit schedule"
    v-model:isVisible="showScheduleEditDialog"
    :fields="reservSchedulesFields"
    :model="selectedSchedule"
    :onSaveAdd="updateSchedule"
    :onCancel="closeScheduleEditModal"
    onSaveAddButtonLabel="Save"
  />

  <EditAddDialog
    header="Edit medical record"
    v-model:isVisible="showMedicalRecordsEditDialog"
    :fields="medicalRecordsFields"
    :model="selectedMedicalRecord"
    :onSaveAdd="updateMedicalRecord"
    :onCancel="closeMedicalRecordEditModal"
    onSaveAddButtonLabel="Save"
  />

  <EditAddDialog
    header="Add schedule"
    v-model:isVisible="showScheduleAddDialog"
    :fields="reservSchedulesFields"
    :model="selectedSchedule"
    :onSaveAdd="addSchedule"
    :onCancel="closeScheduleAddModal"
    onSaveAddButtonLabel="Add"
  />

  <EditAddDialog
    header="Add medical record"
    v-model:isVisible="showMedicalRecordsAddDialog"
    :fields="medicalRecordsFields"
    :model="selectedMedicalRecord"
    :onSaveAdd="addMedicalRecord"
    :onCancel="closeMedicalRecordAddModal"
    onSaveAddButtonLabel="Add"
  />

  <EditAddDialog
    header="Edit animal information"
    v-model:isVisible="showAnimalInfoEditDialog"
    :fields="animalInfoFields"
    :model="selectedAnimalInfo"
    :onSaveAdd="updateAnimalInfo"
    :onCancel="closeAnimalInfoEditDialog"
    onSaveAddButtonLabel="Save"
  />

</template>
  
<script setup>

import { ref, reactive, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axiosClient from '../api/api';
import { useAuthStore, UserRole } from '../store/Authstore';
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
import EditAddDialog from '../components/EditAddDialog.vue';
import ConfirmDialog from 'primevue/confirmdialog';
import { useConfirm } from "primevue/useconfirm";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const user = authStore.getUser;
const userRole = authStore.getRoleId;
const animalInfo = ref({});
const animalSchedules = ref([]);
const animalMedicalRecords = ref([]);

const confirm = useConfirm();

const filteredAnimalInfoFields = computed(() =>
  animalInfoFields.filter(field => field.model !== 'description' && field.model !== 'history')
);

const animalPhoto = computed(() => {
  if(animalInfo.value && animalInfo.value.photo) {
    return `data:image/jpeg;base64,${animalInfo.value.photo}`;
  }

  return null;
});


function confirmReservation(animalName, schedule) {
  confirm.require({
    message: `Are you sure you want to reserve ${animalName} from ${schedule.start_time} to ${schedule.end_time}?`,
    header: 'Confirmation',
    icon: 'pi pi-question',
    accept: async () => {
      try {
        const response = await axiosClient.post(`/volunteer/reservation?volunteer_id=${encodeURIComponent(authStore.getUser.id)}` +
                                                `&animal_id=${encodeURIComponent(route.params.id)}` +
                                                `&start_time=${encodeURIComponent(getFormattedDate(schedule.start_time, true))}` +
                                                `&end_time=${encodeURIComponent(getFormattedDate(schedule.end_time, true))}`,
                                                { withCredentials: true });

        if(response.status === SUCCESS_RESPONSE_CODE) {
          alert('Animal info updated successfully!');
        } else if(response.status === UNKNOWN_OPERATION_RESPONSE_CODE) {
          alert('Error! You have no right to perform this operation!');
        }
      } catch (error) {
        console.error('Error creating reservation: ', error);
        alert('Failed to create reservation');
      }
    },

    reject: () => {
      alert('Not creating reservation');
    }
  })
}

function confirmAnimalDeletion() {
  confirm.require({
    message: `Are you sure you want to delete ${animalInfo?.name}`,
    header: 'Confirmation',
    icon: 'pi pi-question',
    accept: async () => {
      try {
        const response = await axiosClient.delete(`/caretaker/delete_animal?animal_id=${route.params.id}`,
                                                  { withCredentials: true });

        if(response.status === SUCCESS_RESPONSE_CODE) {
          alert('Animal deleted successfully!');
        } else if(response.status === UNKNOWN_OPERATION_RESPONSE_CODE) {
          alert('Error! You have no right to perform this operation!');
        }
      } catch (error) {
        console.error('Error deleting animal: ', error);
        alert('Failed to delete animal');
      }
    },

    reject: () => {
      alert('Not deleting animal');
    }
  })
}

const showAnimalInfoEditDialog = ref(false);
const selectedAnimalInfo = reactive({
  id: null,
  name: '',
  breed: '',
  age: '',
  history: '',
  description: '',
  sex: '',
  // photo: '',
});

const showScheduleEditDialog = ref(false);
const selectedSchedule = reactive({
  id: null,
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

const showScheduleAddDialog = ref(false);
const showMedicalRecordsAddDialog = ref(false);

function getDatePickerPros(showTime) {
  const datePickerProps = {
  dateFormat: "D, dd M yy",
  manualInput: false,
  showIcon: true,
  iconDisplay: "input"
  }

  if(showTime) {
    datePickerProps.showTime = true;
    datePickerProps.showSeconds = true;
    datePickerProps.hourFormat = '24';
  }

  return datePickerProps;
}

const animalInfoFields = [
  { 
    label: 'Name',
    model: 'name',
    component: InputText,
  },
  { 
    label: 'Age',
    model: 'age',
    component: InputText,
  },
  { 
    label: 'Breed',
    model: 'breed',
    component: InputText,
  },
  { 
    label: 'Sex',
    model: 'sex',
    component: InputText,
  },
  { 
    label: 'Description',
    model: 'description',
    component: Textarea,
  },
  { 
    label: 'History',
    model: 'history',
    component: Textarea,
  }
];

const reservSchedulesFields = [
  { 
    label: 'Start date',
    model: 'startDate',
    component: DatePicker,
    props: getDatePickerPros(true)
  },
  { 
    label: 'End date ',
    model: 'endDate',
    component: DatePicker,
    props: getDatePickerPros(true)
  }
];

const medicalRecordsFields = [
  { 
    label: 'Description',
    model: 'description',
    component: Textarea,
  },
  {
    label: 'Examination date',
    model: 'examinationDate',
    component: DatePicker,
    props: getDatePickerPros(false)
  },
  {
    label: 'Examination type',
    model: 'examinationType',
    component: InputText,
  }
];

const SUCCESS_RESPONSE_CODE = 200;
const UNKNOWN_OPERATION_RESPONSE_CODE = 403;

const sendReqAndProcessResponse = async (request, isSchedule, isUpdated, closeModalFn) => {
  try {
    let response;
    
    if(isUpdated) {
      response = await axiosClient.put(request, null, { withCredentials: true });
    } else {
      response = await axiosClient.post(request, null, { withCredentials: true });
    }

    if(response.status === SUCCESS_RESPONSE_CODE) {
      const action = isUpdated ? 'updated' : 'added';
      const recordType = isSchedule ? 'Schedule' : 'Medical record';
      alert(`${recordType} ${action} successfully!`);
    } else if(response.status === UNKNOWN_OPERATION_RESPONSE_CODE) {
      alert('Error! You have no right to perform this operation!');
    }

    closeModalFn();
  } catch (error) {
    const action = isUpdated ? 'updat' : 'add';
    console.error(`Error ${action}ing ${isSchedule ? 'schedule' : 'medical record'}:`, error);
    alert(`Failed to ${action}e ${isSchedule ? 'schedule' : 'medical record'}.`);
  }
}

async function updateAnimalInfo() {
  try {
    const response = await axiosClient.put(`/caretaker/update_animal?animal_id=${encodeURIComponent(selectedAnimalInfo.id)}` +
                                            `&name=${encodeURIComponent(selectedAnimalInfo.name)}` +
                                            `&breed=${encodeURIComponent(selectedAnimalInfo.breed)}` +
                                            `&age=${encodeURIComponent(selectedAnimalInfo.age)}` +
                                            `&history=${encodeURIComponent(selectedAnimalInfo.history)}` +
                                            `&description=${encodeURIComponent(selectedAnimalInfo.description)}` +
                                            `&sex=${encodeURIComponent(selectedAnimalInfo.sex)}`,
                                            null,
                                            { withCredentials: true });

    if(response.status === SUCCESS_RESPONSE_CODE) {
      alert('Animal info updated successfully!');
    } else if(response.status === UNKNOWN_OPERATION_RESPONSE_CODE) {
      alert('Error! You have no right to perform this operation!');
    }

    closeAnimalInfoEditDialog();
  } catch (error) {
    console.error('Error updating animal info: ', error);
    alert('Failed to update animal info');
  }
}

function updateSchedule() {
  const requestUrl = `/caretaker/update_walking_schedule?walking_schedule_id=${encodeURIComponent(selectedSchedule.id)}` +
                     `&start_time=${encodeURIComponent(getFormattedDate(selectedSchedule.startDate, true))}` +
                     `&end_time=${encodeURIComponent(getFormattedDate(selectedSchedule.endDate, true))}`;
                     
  sendReqAndProcessResponse(requestUrl, true, true, closeScheduleEditModal);
  fetchAnimalInfo();
}

function addSchedule() {
  const requestUrl = `/caretaker/walking_schedule?animal_id=${encodeURIComponent(route.params.id)}` +
                      `&start_time=${encodeURIComponent(getFormattedDate(selectedSchedule.startDate, true))}` +
                      `&end_time=${encodeURIComponent(getFormattedDate(selectedSchedule.endDate, true))}`;

  sendReqAndProcessResponse(requestUrl, true, false, closeScheduleAddModal);
  fetchAnimalInfo();
}

function updateMedicalRecord() {
  const requestUrl = `/caretaker/update_medical_record?medical_record_id=${encodeURIComponent(selectedMedicalRecord.id)}` +
                     `&veterinarian_id=${encodeURIComponent(authStore.getUser.id)}` +
                     `&examination_date=${encodeURIComponent(getFormattedDate(selectedMedicalRecord.examinationDate))}` +
                     `&examination_type=${encodeURIComponent(selectedMedicalRecord.examinationType)}` +
                     `&description=${encodeURIComponent(selectedMedicalRecord.description)}`;

  sendReqAndProcessResponse(requestUrl, false, true, closeMedicalRecordEditModal);
  fetchAnimalInfo();
};

function addMedicalRecord() {
  const requestUrl = `/veterinarian/create_medical_record?animal_id=${encodeURIComponent(route.params.id)}` +
                     `&veterinarian_id=${encodeURIComponent(authStore.getUser.id)}` +
                     `&description=${encodeURIComponent(selectedMedicalRecord.description)}` +
                     `&examination_date=${encodeURIComponent(getFormattedDate(selectedMedicalRecord.examinationDate))}` +
                     `&examination_type=${encodeURIComponent(selectedMedicalRecord.examinationType)}`;
                     
  sendReqAndProcessResponse(requestUrl, false, false, closeMedicalRecordAddModal);
  fetchAnimalInfo();
};

const openAnimalInfoEditModal = async (animalInfo) => {
  selectedAnimalInfo.id = animalInfo.id;
  selectedAnimalInfo.name = animalInfo.name;
  selectedAnimalInfo.breed = animalInfo.breed;
  selectedAnimalInfo.age = animalInfo.age;
  selectedAnimalInfo.history = animalInfo.history;
  selectedAnimalInfo.description = animalInfo.description;
  selectedAnimalInfo.sex = animalInfo.sex;

  showAnimalInfoEditDialog.value = true;
};

const closeAnimalInfoEditDialog = async () => {
  showAnimalInfoEditDialog.value = false;
};

const openScheduleAddModal = async (schedule) => {
  selectedSchedule.id = 1;
  selectedSchedule.startDate = undefined;
  selectedSchedule.endDate = undefined;
  // selectedSchedule.startDate = 1;
  // selectedSchedule.endDate = 1;


  showScheduleAddDialog.value = true;
};

const closeScheduleAddModal = async () => {
  showScheduleAddDialog.value = false;
};

const openMedicalRecordAddModal = async (schedule) => {
  selectedMedicalRecord.id = 1;
  selectedMedicalRecord.description = undefined;
  selectedMedicalRecord.examinationDate = undefined;
  selectedMedicalRecord.examinationType = undefined;

  showMedicalRecordsAddDialog.value = true;
};

const closeMedicalRecordAddModal = async () => {
  showMedicalRecordsAddDialog.value = false;
};

const openScheduleEditModal = async (schedule) => {
  selectedSchedule.startDate = schedule.start_time;
  selectedSchedule.endDate = schedule.end_time;

  selectedSchedule.id = schedule.id;

  showScheduleEditDialog.value = true;
};

const closeScheduleEditModal = async () => {
  showScheduleEditDialog.value = false;
};

const openMedicalRecordEditModal = async (medicalRecord) => {
  selectedMedicalRecord.id = medicalRecord.id;
  selectedMedicalRecord.description = medicalRecord.description;
  selectedMedicalRecord.examinationDate = medicalRecord.examination_date;
  selectedMedicalRecord.examinationType = medicalRecord.examination_type;

  showMedicalRecordsEditDialog.value = true;
};

const closeMedicalRecordEditModal = async () => {
  showMedicalRecordsEditDialog.value = false;
};

const fetchAnimalInfo = async () => {
  try {
    const response = await axiosClient.get(`/animal/info?animal_id=${encodeURIComponent(route.params.id)}`);
    animalInfo.value = response.data.animal;

    animalSchedules.value = response.data.schedules.map(schedule => {
      const startDateTimePart = schedule.start_time.replace(" GMT", "");
      const endtDateTimePart = schedule.end_time.replace(" GMT", "");

      return {
        ...schedule,
        start_time: startDateTimePart,
        end_time: endtDateTimePart
      };
    });

    animalMedicalRecords.value = response.data.medical_records.map(record => {
      const datePart = record.examination_date.split(' ').slice(0, 4).join(' ');

      return {
        ...record,
        examination_date: datePart
      };
    });
  } catch (error) {
    console.error('Error fetching animal data:', error);
  }
}

onMounted(fetchAnimalInfo);

</script>
  
<style scoped>

.non-prime-animal-info {
  color: var(--p-fieldset-color);
}

.animal-schedules {
  grid-row: 2 / span 1;
  justify-content: center;
  align-items: center;
  width: 100%;
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

.animal-info {
  display: grid;
  grid-template-columns: 0.2fr 1fr;
  gap: 20px;
}

.tags-column {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: 8px;
  justify-content: space-between;
}

.tags {
  margin-bottom: 5px;
}

.animal-fieldsets {
  display: flex;
  flex-direction: column;
  gap: 0px;
  justify-content: space-between;
}

fieldset {
  width: 100%;
  height: 100%;
  max-width: 800px;
  word-break: break-word;
  white-space: normal;
  overflow-wrap: break-word;
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
  border-radius: 10px;
}

.full-width-table .p-column-title, .full-width-table td {
  white-space: normal;
  word-break: break-word;
}

.full-width-table td {
  max-width: 100%;
  padding: 10px;
}

</style>
  