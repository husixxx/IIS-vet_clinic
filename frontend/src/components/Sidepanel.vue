<template>
  <div class="card flex flex-col items-center gap-4">
    <!-- Name input without label -->
    <div class="input-container">
      <input
        type="text"
        placeholder="Insert Name"
        v-model="filterItems[0].value"
        class="p-inputtext input-field"
      />
    </div>

    <!-- Age input without label -->
    <div class="input-container">
      <input
        type="text"
        placeholder="Insert Age"
        v-model="filterItems[1].value"
        class="p-inputtext input-field"
      />
    </div>

    <!-- Dropdown for Breed -->
    <div class="input-container">
      <Dropdown
        :options="filterItems[2].options"
        v-model="filterItems[2].value"
        placeholder="Select Breed"
        class="p-dropdown"
      />
    </div>

    <!-- Availability input without label -->
    <div class="input-container">
      <input
        type="text"
        placeholder="Insert Availability"
        v-model="filterItems[3].value"
        class="p-inputtext input-field"
      />
    </div>

    <!-- Search Button -->
    <div class="input-container">
      <Button type="button" label="Search" class="p-button-success input-field" @click="search" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';

// List of filters
const filterItems = ref([
  { key: '0', label: 'Name', value: '', type: 'text' },
  { key: '1', label: 'Age', value: '', type: 'text' },
  { key: '2', label: 'Breed', value: '', type: 'dropdown', options: [
    { label: 'Dog', value: 'dog' },
    { label: 'Cat', value: 'cat' },
    { label: 'Rabbit', value: 'rabbit' }
  ]},
  { key: '3', label: 'Availability', value: '', type: 'text' }
]);

// Search function to handle search logic
const search = () => {
  console.log('Search filters:', filterItems.value);
};
</script>

<style scoped>
.input-container {
  width: 100%;
  max-width: 350px; /* Increase the width for better visibility */
  margin-bottom: 10px;
}

.input-field {
  width: 100%;
  height: 40px; /* Set inputs and button to match the original height */
  padding: 8px;
  border-radius: 4px;
  box-sizing: border-box;
}

.p-inputtext {
  height: 38px; /* Adjust the input height slightly to match the dropdown */
}

.p-button-success {
  width: 100%;
  height: 38px; /* Ensure the button height is consistent with the inputs */
}

.p-dropdown {
  width: 100%;
}
</style>
