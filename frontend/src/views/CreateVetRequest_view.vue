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
          <div class="p-field send-vet-request">
            <Button label="Send request" @click="handleSendVetRequest" class="w-full" />
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

const veterinarians = ref([]);
const filteredVeterinarians = ref([]);
const selectedVeterinarian = ref(null);

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

</script>

<style scoped>

.w-full {
  width: 100%;
}

</style>
