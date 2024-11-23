<template>
  <div class="card flex flex-col items-center gap-4">
    <!-- Name input -->
    <div class="input-container">
      <InputText
        id="name"
        type="text"
        v-model="filters.name"
        placeholder="Insert Name"
        class="p-inputtext input-field"
        :maxlength="30"
        />
        <small v-if="filters.name.length >= 30" class="max-input-text">
          Maximum 50 characters allowed
        </small>
    </div>

    <!-- Age input -->
    <div class="input-container">
      <InputText
        id="age"
        type="text"
        v-model="filters.age"
        placeholder="Insert Age"
        class="p-inputtext input-field no-spinner"
        :maxlength="3"
        @keypress="allowOnlyIntegers"
      />
      <small v-if="filters.age.length >= 3" class="max-input-text">
        Maximum 3 characters allowed
      </small>
    </div>

    <!-- Dropdown for Breed -->
    <div class="input-container">
      <Dropdown
        id="breed"
        v-model="filters.breed"
        :options="breedOptions"
        optionLabel="label"
        placeholder="Select Breed"
        class="p-dropdown w-full"
      />
    </div>

    <!-- Dropdown for Availability -->
    <div class="input-container">
      <Dropdown
        id="availability"
        v-model="filters.availability"
        :options="availabilityOptions"
        optionLabel="label"
        placeholder="Select Availability"
        class="p-dropdown w-full"
      />
    </div>

    <!-- Search Button -->
    <div class="input-container">
      <Button
        type="button"
        label="Search"
        class="p-button-success input-field"
        @click="applyFilter"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted,computed } from 'vue';
import axiosClient from '../api/api';  // Ensure axiosClient is correctly imported
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';

// Define the emit event
const emit = defineEmits(['filter-animals']);

const allowOnlyIntegers = (event) => {
  // Ak nie je stlačený číselný znak, zablokuj vstup
  if (!/^[0-9]$/.test(event.key)) {
    event.preventDefault();
  }
};

// Set up filter states
const filters = ref({
  name: '',
  age: '',
  breed: '',
  availability: '',
});

// Dynamic breed options
const breedOptions = ref([]);

// Availability options
const availabilityOptions = ref([
  { label: 'All', value: '' },   // Default option
  { label: 'Yes', value: true },
  { label: 'No', value: false },
]);

// Fetch breed options from API
const fetchBreeds = async () => {
  try {
    const response = await axiosClient.get('/animal/breeds',{withCredentials: true});
    breedOptions.value = [
      { label: 'All', value: '' },  // Default option for breed
      ...response.data.map(breed => ({
        label: breed,   // The breed label to display
        value: breed    // The actual breed value
      })),
    ];
  } catch (error) {
    console.error('Error fetching breeds:', error);
  }
};

// Fetch breeds on component mount
onMounted(() => {
  fetchBreeds();
});

// Apply filters and emit to the parent component
const applyFilter = () => {
  const filtersToSend = {
    name: filters.value.name,
    age: filters.value.age,
    breed: filters.value.breed.value,
    availability: filters.value.availability.value,
  };

  emit('filter-animals', filtersToSend);
};
</script>

<style scoped>
.input-container {
  width: 100%;
  max-width: 200px; /* Width for filter panel */
  margin-bottom: 10px;
}

.input-field {
  width: 100%;
  height: 40px; /* Height for inputs and button */
  padding: 8px;
  border-radius: 4px;
  box-sizing: border-box;
}

.p-inputtext {
  height: 38px; /* Adjust height to match dropdown */
}

.p-button-success {
  width: 100%;
  height: 38px; /* Consistent height with inputs */
}

.p-dropdown {
  width: 100%;
}
</style>
