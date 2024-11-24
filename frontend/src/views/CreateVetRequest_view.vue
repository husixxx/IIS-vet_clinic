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
                          optionLabel="nameAndUsername" dropdown
                          :invalid="!selectedVeterinarian"
                          placeholder="Enter vet's name or username"/>
          </div>
          <div class="p-field input-group">
            <label for="description" class="input-label">Description</label>
            <Textarea id="description" v-model="description" placeholder="Enter request's description" class="input-text" rows="5" :invalid="!description"/>
          </div>
          <div class="p-field input-group">
            <label for="date" class="input-label">Date</label>
            <DatePicker class="input-text" v-model="date" :manualInput="false" dateFormat="D, dd M yy" showIcon fluid iconDisplay="input" :invalid="!date" hourFormat="24" placeholder="Enter request's date" :minDate="new Date()"/>
          </div>
          <div class="p-field send-vet-request">
            <Button label="Send request" @click="handleSendVetRequest" class="w-full" icon="pi pi-send" :disabled=" !selectedVeterinarian || !description || !date || !isValidVetUsername()" />
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
import { getFormattedDate } from '../utils/date';
import { useRoute } from 'vue-router';

const veterinarians = ref([]);
const filteredVeterinarians = ref([]);
const selectedVeterinarian = ref(null);
const description = ref('');
const date = ref(null);
const SUCCESS_RESPONSE_CODE = ref(200);
const UNKNOWN_OPERATION_RESPONSE_CODE = ref(403);
const route = useRoute();

onMounted(async () => {
    try {
        const response = await axiosClient.get('/caretaker/veterinarians', { withCredentials: true});

        if(response.status === UNKNOWN_OPERATION_RESPONSE_CODE) {
          alert('Error! You have no right to perform this operation!');
        }

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

const isValidVetUsername = () => {
  console.log(selectedVeterinarian?.value?.username)
  return veterinarians.value.some(vet => vet.username === selectedVeterinarian?.value?.username);
}

const handleSendVetRequest = async () => {
  try {
    console.log(date.value);
    const response = await axiosClient.post(
      `/caretaker/vet_request?animal_id=${encodeURIComponent(route.params.animalId)}` + 
      `&veterinarian_username=${encodeURIComponent(selectedVeterinarian.value.username)}` +
      `&request_date=${encodeURIComponent(getFormattedDate(date.value, true))}&description=${encodeURIComponent(description.value)}`,
      null,
      { withCredentials: true}
    );

    if(response.status === SUCCESS_RESPONSE_CODE.value) {
      selectedVeterinarian.value = '';
      description.value = '';
      date.value = '';
      alert('Veterinarian request created successfully!');
    } else if(response.status === UNKNOWN_OPERATION_RESPONSE_CODE) {
      alert('Error! You have no right to perform this operation!');
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
