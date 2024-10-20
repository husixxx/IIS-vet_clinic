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
      />
    </div>

    <!-- Age input -->
    <div class="input-container">
      <InputText
        id="age"
        type="text"
        v-model="filters.age"
        placeholder="Insert Age"
        class="p-inputtext input-field"
      />
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
import { ref, defineEmits } from 'vue';
import InputText from 'primevue/inputtext';
import Dropdown from 'primevue/dropdown';
import Button from 'primevue/button';

// Set up filter states
const filters = ref({
  name: '',
  age: '',
  breed: ''
});

// Breed options
const breedOptions = [
  { label: 'Dog', value: 'dog' },
  { label: 'Cat', value: 'cat' },
  { label: 'Rabbit', value: 'rabbit' },
];

// Apply filters and emit to the parent component
const applyFilter = () => {
  emit('filter-animals', filters.value);
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
