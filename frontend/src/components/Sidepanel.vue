<template>
  <div class="card flex flex-col items-center gap-4">
    <!-- Name input -->
    <div class="input-container">
      <InputText
        id="name"
        type="text"
        v-model="filterItems[0].value"
        placeholder="Insert Name"
        class="p-inputtext input-field"
      />
    </div>

    <!-- Age input -->
    <div class="input-container">
      <InputText
        id="age"
        type="text"
        v-model="filterItems[1].value"
        placeholder="Insert Age"
        class="p-inputtext input-field"
      />
    </div>

    <!-- Dropdown for Breed -->
    <div class="input-container">
      <Dropdown
        id="breed"
        v-model="filterItems[2].value"
        :options="filterItems[2].options"
        optionLabel="label"
        placeholder="Select Breed"
        class="p-dropdown w-full"
      />
    </div>

    <!-- Availability input -->
    <div class="input-container">
      <InputText
        id="availability"
        type="text"
        v-model="filterItems[3].value"
        placeholder="Insert Availability"
        class="p-inputtext input-field"
      />
    </div>

    <!-- Search Button -->
    <div class="input-container">
      <Button
        type="button"
        label="Search"
        class="p-button-success input-field"
        @click="search"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Button from "primevue/button";
import Dropdown from "primevue/dropdown";
import InputText from "primevue/inputtext";

// List of filters
const filterItems = ref([
  { key: "0", label: "Name", value: "", type: "text" },
  { key: "1", label: "Age", value: "", type: "text" },
  { key: "2", label: "Breed", value: "", type: "dropdown", options: [
    { label: "Dog", value: "dog" },
    { label: "Cat", value: "cat" },
    { label: "Rabbit", value: "rabbit" },
  ] },
  { key: "3", label: "Availability", value: "", type: "text" },
]);

// Search function to handle search logic
const search = () => {
  console.log("Search filters:", filterItems.value);
};
</script>

<style scoped>
.input-container {
  width: 100%;
  max-width: 200px; /* Zachované pre užší panel */
  margin-bottom: 10px;
}

.input-field {
  width: 100%;
  height: 40px; /* Nastavená výška pre inputy a tlačidlá */
  padding: 8px;
  border-radius: 4px;
  box-sizing: border-box;
}

.p-inputtext {
  height: 38px; /* Jemná úprava výšky, aby zodpovedala dropdownu */
}

.p-button-success {
  width: 100%;
  height: 38px; /* Konzistentná výška tlačidla s inputmi */
  background-color: #10b981; /* Set the background color */
}

.p-dropdown {
  width: 100%;
}
</style>
