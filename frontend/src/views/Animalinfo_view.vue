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
              <Column v-if="authStore.getRoleId === UserRole.Volunteer" header="" style="width: 10%; text-align: right;" headerStyle="text-align: right; padding-right: 30px;">
                <template #body="slotProps">
                  <Button
                    label="Make reservation"
                   
                    class="p-button-warning"
                  />
                </template>
              </Column>
              <Column v-if="authStore.getRoleId === UserRole.Caretaker" header="" style="width: 10%; text-align: right;" headerStyle="text-align: right; padding-right: 30px;">
                <template #body="slotProps">
                  <Button
                    label="Edit schedule"
                   
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
</template>
  
<script setup>

import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axiosClient from '../api/api';
import { useAuthStore, UserRole } from '../store/Authstore';  // Ensure correct import of your AuthStore
import Fieldset from 'primevue/fieldset';
import DataTable from 'primevue/datatable';
import Card from 'primevue/card';
import Column from 'primevue/column';
import Button from 'primevue/button';

const route = useRoute();
const authStore = useAuthStore();
const user = authStore.getUser;
const userRole = authStore.getRoleId;
const animalInfo = ref();
const animalSchedules = ref([]);
const animalMedicalRecords = ref([]);

// const showEditDialog = ref(false);
// const selectedSchedule = reactive({
//   id: null,
//   animalId: null,
//   startTime: '',
//   endTime: ''
// });

// const reservSchedulesFields = [
//   { id: 'startDate', label: 'Start date', model: 'startDate', component: InputText },
//   { id: 'endtDate', label: 'endDate', model: 'endDate', component: InputText }
//   // { id: 'username', label: 'Username', model: 'username', component: InputText },
//   // { id: 'password', label: 'Password', model: 'password', component: InputText, props: { type: 'password' } },
//   // { id: 'verified', label: 'Verified', model: 'verified', component: Dropdown, props: { options: verifiedOptions, optionLabel: 'label' } },
//   // { id: 'role_id', label: 'Role', model: 'role_id', component: Dropdown, props: { options: roleOptions, optionLabel: 'label' } }
// ];

onMounted(async () => {
  try {
    const response = await axiosClient.get(`/animal/info?animal_id=${encodeURIComponent(route.params.id)}`);
    console.log(response.data);
    animalInfo.value = response.data;
    animalSchedules.value = animalInfo.value.schedules;
    animalMedicalRecords.value = animalInfo.value.medical_records;
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
  