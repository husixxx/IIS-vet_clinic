<template>
  <div class="create-vet-request-container">
    <Card>
      <template #title>Create request</template>
      <template #content>
        <div class="p-fluid">
          <div class="p-field input-group">
            <label for="veterinarian" class="input-label">Veterinarian</label>
            <AutoComplete v-model="selectedVeterinarian" 
                          :suggestions="filteredVeterinarians" 
                          @complete="searchVeterinarians" 
                          :virtualScrollerOptions="{ itemSize: 50 }"
                          optionLabel="nameAndUsername" dropdown />
          </div>
          <div class="p-field input-group">
            <label for="description" class="input-label">Description</label>
            <Textarea id="description" v-model="description" placeholder="Enter request's description" class="input-text" rows="5" />
          </div>
          <div class="p-field input-group">
            <label for="date" class="input-label">Date</label>
            <DatePicker class="input-text" v-model="date" :manualInput="false" dateFormat="yy-mm-dd" showIcon fluid iconDisplay="input" />
          </div>
          <div class="p-field send-vet-request">
            <Button label="Send request" @click="handleSendVetRequest" class="w-full" icon="pi pi-send" />
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup>

import { ref, onMounted } from 'vue';
import Card from 'primevue/card';
import Button from 'primevue/button';
import axiosClient from '../api/api';
import AutoComplete  from 'primevue/autocomplete';
import Textarea from 'primevue/textarea';
import DatePicker from 'primevue/datepicker';
import 'primeicons/primeicons.css'

const veterinarians = ref([]);
const filteredVeterinarians = ref([]);
const selectedVeterinarian = ref(null);
const animalId = ref(7); // TODO CHANGE IT!!!
const description = ref('');
const date = ref(null);
const SUCCESS_RESPONSE_CODE = ref(200);

onMounted(async () => {
    try {
        const response = await axiosClient.get('/caretaker/veterinarians');
        veterinarians.value = response.data.map(vet => ({
          ...vet,
          nameAndUsername: `${vet.name} (${vet.username})`
        }));
        console.log(veterinarians);
    } catch (error) {
        console.error('Error fetching volunteers:', error);
    }
});

const searchVeterinarians = (event) => {
  const query = event.query.toLowerCase();
  filteredVeterinarians.value = veterinarians.value.filter(vet =>
    vet.name.toLowerCase().includes(query) || vet.username.toLowerCase().includes(query)
  );
};

// function getCurrentDate() {
//   const today = new Date();

//   const year = today.getFullYear();
//   const month = String(today.getMonth() + 1).padStart(2, '0');
//   const day = String(today.getDate()).padStart(2, '0');

//   return  `${year}-${month}-${day}`;
// }

function getFormattedDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

const handleSendVetRequest = async () => {
  try {
    console.log(date.value);
    const response = await axiosClient.post(
      `/caretaker/vet_request?animal_id=${encodeURIComponent(animalId.value)}` + 
      `&veterinarian_username=${encodeURIComponent(selectedVeterinarian.value.username)}` +
      `&request_date=${encodeURIComponent(getFormattedDate(date.value))}&description=${encodeURIComponent(description.value)}`
    );

    if(response.status === SUCCESS_RESPONSE_CODE.value) {
      selectedVeterinarian.value = '';
      description.value = '';
      date.value = '';
      alert('Veterinarian request created successfully!');
    }

  } catch (error) {
    console.error('Error sending vet request:', error);
    alert('Failed to send vet request.');
  }
}

</script>

<style scoped>

.w-full {
  width: 100%;
}

</style>
