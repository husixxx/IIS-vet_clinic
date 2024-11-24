<template>
  <div class="main-content" v-if="animalInfo.name">
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
            <DataTable :value="animalSchedules" class="full-width-table" tableStyle="width: 100%" v-if="animalSchedules.length">
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
                  <Button
                    label="Delete schedule"
                    @click="confirmScheduleDeletion(slotProps.data)"
                    class="p-button-danger"
                    style="margin-top: 5px;"
                  />
                </template>
              </Column>
            </DataTable>
            <h1 v-else style="text-align: center; left: 50%; top: 50%;">No avaliable schedules</h1>
          </div>
        </template>
      </Card>
    </div>

    <div class="animal-info">
      <div class="tags-column">
        <div class="tags non-prime-animal-info" v-for="(field, index) in filteredAnimalInfoFields" :key="index">
          <strong>{{ field.label }}:</strong> {{ animalInfo?.[field.model] }}
        </div>

        <div v-if="authStore.getRoleId === UserRole.Volunteer || authStore.getRoleId === UserRole.Veterinarian || authStore.getRoleId === UserRole.Caretaker || authStore.getRoleId === UserRole.Admin" class="tags non-prime-animal-info">
          <strong>ID:</strong> {{ animalInfo?.id }}
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
            <DataTable :value="animalMedicalRecords" class="full-width-table" tableStyle="width: 100%" v-if="animalMedicalRecords.length">
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
            <h1 v-else style="text-align: center; left: 50%; top: 50%;">No medical records</h1>
          </div>
        </template>
      </Card>
    </div>
  </div>

  <div v-else class="main-content">
    <h1 style="text-align: center; left: 50%; top: 50%;">Animal not found</h1>
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
import InputNumber from 'primevue/inputnumber';
import Dropdown from 'primevue/dropdown';

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
  animalInfoFields.filter(field => field.model !== 'description' && field.model !== 'history' && field.model !== 'photo')
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
        let response = await axiosClient.post(`/volunteer/reservation?volunteer_id=${encodeURIComponent(authStore.getUser.id)}` +
                                                `&animal_id=${encodeURIComponent(route.params.id)}` +
                                                `&start_time=${encodeURIComponent(getFormattedDate(schedule.start_time, true))}` +
                                                `&end_time=${encodeURIComponent(getFormattedDate(schedule.end_time, true))}`,
                                                { withCredentials: true });

        if(response.status === SUCCESS_RESPONSE_CODE) {
          alert('Animal info updated successfully!');
        } else if(response.status === UNKNOWN_OPERATION_RESPONSE_CODE) {
          alert('Error! You have no right to perform this operation!');
        }

        // response = await axiosClient.delete(`/volunteer/delete_walking_schedule?walking_schedule_id=${encodeURIComponent(schedule.id)}`,
        //                                     { withCredentials: true });

        // await fetchAnimalInfo();
      } catch (error) {
        // console.error('Error creating reservation: ', error);
        alert('Failed to make reservation');
      }
    },

    reject: () => {
      alert('Not making reservation');
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

        // await router.push({ name: 'animal'});
        router.push({ name: 'Animal'});
      } catch (error) {
        // console.error('Error deleting animal: ', error);
        alert('Failed to delete animal', error);
      }
    },

    reject: () => {
      alert('Not deleting animal');
      // console.log(router.getRoutes());
    }
  })
}

function confirmScheduleDeletion(schedule) {
  confirm.require({
    message: `Are you sure you want to delete this walking schedule?`,
    header: 'Confirmation',
    icon: 'pi pi-question',
    accept: async () => {
      try {
        const response = await axiosClient.delete(`/caretaker/delete_walking_schedule?walking_schedule_id=${encodeURIComponent(schedule.id)}`,
                                            { withCredentials: true });

        if(response.status === SUCCESS_RESPONSE_CODE) {
          alert('Walking schedule deleted successfully!');
        }

        await fetchAnimalInfo();
      } catch (error) {
        alert('Failed to delete walking schedule');
      }
    },

    reject: () => {
      alert('Not deleting walking schedule');
      // console.log(router.getRoutes());
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
  photo: '',
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
  iconDisplay: "input",
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
    props: {
      placeholder: 'Enter animal\'s name'
    }
  },
  { 
    label: 'Breed',
    model: 'breed',
    component: InputText,
    props: {
      placeholder: 'Enter animal\'s breed'
    }
  },
  { 
    label: 'Age',
    model: 'age',
    component: InputNumber,
    props: {
      placeholder: 'Enter animal\'s age'
    }
  },
  { 
    label: 'Sex',
    model: 'sex',
    component: Dropdown,
    props: {
      placeholder: 'Enter animal\'s sex',
      options: [
        'Male',
        'Female',
      ],
    }
  },
  { 
    label: 'Photo (JPEG only)',
    model: 'photo', // No v-model as it's a plain file input
    component: 'file', // Indicates that this is a file input
    props: {
      accept: 'image/jpeg',
    }
  },
  { 
    label: 'Description',
    model: 'description',
    component: Textarea,
    props: {
      placeholder: 'Enter animal\'s description'
    }
  },
  { 
    label: 'History',
    model: 'history',
    component: Textarea,
    props: {
      placeholder: 'Enter animal\'s history'
    }
  }
];

const reservSchedulesFields = [
  { 
    label: 'Start date',
    model: 'startDate',
    component: DatePicker,
    props: {
      ...getDatePickerPros(true),
      placeholder: "Enter start date",
      minDate: new Date(),
    }
  },
  { 
    label: 'End date ',
    model: 'endDate',
    component: DatePicker,
    props: {
      ...getDatePickerPros(true),
      placeholder: "Enter end date",
      minDate: new Date(),
    }
  }
];

const medicalRecordsFields = [
  { 
    label: 'Description',
    model: 'description',
    component: Textarea,
    props: {
      placeholder: 'Enter description'
    }
  },
  {
    label: 'Examination date',
    model: 'examinationDate',
    component: DatePicker,
    props: {
      ...getDatePickerPros(false),
      placeholder: "Enter examination date",
      minDate: new Date()
    }
  },
  {
    label: 'Examination type',
    model: 'examinationType',
    component: InputText,
    props: {
      placeholder: 'Enter examination type'
    }
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
    // console.error(`Error ${action}ing ${isSchedule ? 'schedule' : 'medical record'}:`, error);
    alert(`Failed to ${action}e ${isSchedule ? 'schedule' : 'medical record'}.`);
  }
}

async function updateAnimalInfo() {
  try {
    // Prepare form data with the animal details
    const formData = new FormData();
    formData.append('animal_id', selectedAnimalInfo.id);
    formData.append('name', selectedAnimalInfo.name);
    formData.append('breed', selectedAnimalInfo.breed);
    formData.append('age', selectedAnimalInfo.age);
    formData.append('sex', selectedAnimalInfo.sex);
    formData.append('history', selectedAnimalInfo.history);
    formData.append('description', selectedAnimalInfo.description);
    
    // Append the photo file if available
    if(selectedAnimalInfo.photo) {
      formData.append('photo', selectedAnimalInfo.photo);
    }

    // Send form data using POST request
    const response = await axiosClient.put('/caretaker/update_animal', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      withCredentials: true  // Zabezpečí, že cookies budú odoslané a prijaté
    });

    if(response.status === SUCCESS_RESPONSE_CODE) {
      alert('Animal info updated successfully!');
    } else if(response.status === UNKNOWN_OPERATION_RESPONSE_CODE) {
      alert('Error! You have no right to perform this operation!');
    }

    await fetchAnimalInfo();
    closeAnimalInfoEditDialog();

  } catch (error) {
    // console.error('Error updating animal info: ', error);
    alert('Failed to update animal info');
  }
}

async function updateSchedule() {
  const startDate = new Date(selectedSchedule.startDate);
  const endDate = new Date(selectedSchedule.endDate);
  // console.log(isDifferenceAtMostTwoHours(selectedSchedule.startDate, selectedSchedule.endDate))
  if(startDate >= endDate || !isDifferenceAtMostTwoHours(selectedSchedule.startDate, selectedSchedule.endDate)) {
    alert('Error! Start date can\'t be greater or equal than end date! The difference between time must be at most 2 hours!')
    selectedSchedule.startDate = undefined;
    return;
  }


  // console.log(selectedSchedule.startDate, getFormattedDate(selectedSchedule.startDate, true))
  const requestUrl = `/caretaker/update_walking_schedule?walking_schedule_id=${encodeURIComponent(selectedSchedule.id)}` +
                     `&start_time=${encodeURIComponent(getFormattedDate(selectedSchedule.startDate, true))}` +
                     `&end_time=${encodeURIComponent(getFormattedDate(selectedSchedule.endDate, true))}`;
                     
  await sendReqAndProcessResponse(requestUrl, true, true, closeScheduleEditModal);
  await fetchAnimalInfo();
}

function isDifferenceAtMostTwoHours(startDate, endDate) {
  const start = new Date(startDate);
  const end = new Date(endDate);

  // Calculate the absolute difference in milliseconds
  const differenceInMilliseconds = Math.abs(end - start);

  // Convert milliseconds to hours
  const differenceInHours = differenceInMilliseconds / (1000 * 60 * 60);

  // Check if the difference is at most 2 hours
  return differenceInHours <= 2;
}

async function addSchedule() {
  const startDate = new Date(selectedSchedule.startDate);
  const endDate = new Date(selectedSchedule.endDate);
  // console.log(isDifferenceAtMostTwoHours(selectedSchedule.startDate, selectedSchedule.endDate))
  if(startDate >= endDate || !isDifferenceAtMostTwoHours(selectedSchedule.startDate, selectedSchedule.endDate)) {
    alert('Error! Start date can\'t be greater or equal than end date! The difference between time must be at most 2 hours!')
    selectedSchedule.startDate = undefined;
    return;
  }

  const requestUrl = `/caretaker/walking_schedule?animal_id=${encodeURIComponent(route.params.id)}` +
                      `&start_time=${encodeURIComponent(getFormattedDate(selectedSchedule.startDate, true))}` +
                      `&end_time=${encodeURIComponent(getFormattedDate(selectedSchedule.endDate, true))}`;

  await sendReqAndProcessResponse(requestUrl, true, false, closeScheduleAddModal);
  await fetchAnimalInfo();
}

async function updateMedicalRecord() {
  const requestUrl = `/caretaker/update_medical_record?medical_record_id=${encodeURIComponent(selectedMedicalRecord.id)}` +
                     `&veterinarian_id=${encodeURIComponent(authStore.getUser.id)}` +
                     `&examination_date=${encodeURIComponent(getFormattedDate(selectedMedicalRecord.examinationDate))}` +
                     `&examination_type=${encodeURIComponent(selectedMedicalRecord.examinationType)}` +
                     `&description=${encodeURIComponent(selectedMedicalRecord.description)}`;

  await sendReqAndProcessResponse(requestUrl, false, true, closeMedicalRecordEditModal);
  await fetchAnimalInfo();
};

async function addMedicalRecord() {
  const requestUrl = `/veterinarian/create_medical_record?animal_id=${encodeURIComponent(route.params.id)}` +
                     `&veterinarian_id=${encodeURIComponent(authStore.getUser.id)}` +
                     `&description=${encodeURIComponent(selectedMedicalRecord.description)}` +
                     `&examination_date=${encodeURIComponent(getFormattedDate(selectedMedicalRecord.examinationDate))}` +
                     `&examination_type=${encodeURIComponent(selectedMedicalRecord.examinationType)}`;
                     
  await sendReqAndProcessResponse(requestUrl, false, false, closeMedicalRecordAddModal);
  await fetchAnimalInfo();
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

    // console.log(animalInfo)

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
    // console.log(animalInfo.value)
    alert('Error fetching animal data:', error);
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
  