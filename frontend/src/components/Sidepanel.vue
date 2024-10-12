<template>
    <div class="card flex flex-col items-center gap-4">
      <!-- Toggle button for expanding or collapsing all -->
      <Button type="button" label="Toggle All" text @click="toggleAll" />
      
      <!-- Render the filter options dynamically -->
      <div v-for="(item, index) in filterItems" :key="index" class="w-full md:w-80">
        <Button type="button" :label="item.label" text @click="toggleInput(item.key)" class="w-full" />
        <div v-if="expandedKeys[item.key]" class="input-wrapper mt-2">
          <input
            type="text"
            :placeholder="`Enter ${item.label}`"
            v-model="item.value"
            class="p-inputtext w-full"
          />
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import Button from 'primevue/button';
  
  // List of filters
  const filterItems = ref([
    { key: '0', label: 'Name', value: '' },
    { key: '1', label: 'Location of founding', value: '' },
    { key: '2', label: 'Age', value: '' },
    { key: '3', label: 'Breed', value: '' },
    { key: '4', label: 'Medical Records', value: '' },
    { key: '5', label: 'Availability', value: '' }
  ]);
  
  // Expanded state to track which inputs are visible
  const expandedKeys = ref({});
  
  // Toggle the display of the input field for a specific filter
  const toggleInput = (key) => {
    expandedKeys.value[key] = !expandedKeys.value[key];
  };
  
  // Expand all or collapse all inputs
  const toggleAll = () => {
    if (Object.keys(expandedKeys.value).length) {
      collapseAll();
    } else {
      expandAll();
    }
  };
  
  const expandAll = () => {
    filterItems.value.forEach((item) => {
      expandedKeys.value[item.key] = true;
    });
  };
  
  const collapseAll = () => {
    expandedKeys.value = {};
  };
  </script>
  
  <style scoped>
  .input-wrapper {
    display: flex;
    justify-content: center;
  }
  
  input {
    border: 1px solid #ccc;
    padding: 8px;
    border-radius: 4px;
  }
  
  button {
    margin-bottom: 10px;
  }
  </style>
  