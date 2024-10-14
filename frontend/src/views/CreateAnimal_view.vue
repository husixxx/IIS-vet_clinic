<template>
    <div class="sign-up-container">
      <Card class="centered-card">
        <template #title>
          <div class="title-center">Create Animal</div>
        </template>
        <template #content>
          <div class="p-fluid">
            <!-- Form inputs -->
            <div class="p-field input-group">
              <label for="name" class="input-label">Name</label>
              <InputText id="name" v-model="name" placeholder="Enter the animal's name" class="input-text" />
            </div>
  
            <div class="p-field input-group">
              <label for="breed" class="input-label">Breed</label>
              <InputText id="breed" v-model="breed" placeholder="Enter the breed" class="input-text" />
            </div>
  
            <div class="p-field input-group">
              <label for="age" class="input-label">Age</label>
              <InputNumber id="age" v-model="age" placeholder="Enter the age" class="input-text" />
            </div>
  
            <div class="p-field input-group">
              <label for="sex" class="input-label">Sex</label>
              <Dropdown v-model="sex" :options="sexOptions" placeholder="Select sex" class="input-text" />
            </div>
  
            <div class="p-field input-group">
              <label for="history" class="input-label">History</label>
              <Textarea id="history" v-model="history" placeholder="Enter animal's history" class="input-text" rows="5" />
            </div>
  
            <div class="p-field input-group">
              <label for="description" class="input-label">Description</label>
              <Textarea id="description" v-model="description" placeholder="Enter description" class="input-text" rows="5" />
            </div>
  
            <!-- Submit Button -->
            <div class="p-field sign-up-button">
              <Button label="Create Animal" icon="pi pi-check" @click="handleCreateAnimal" class="w-full" />
            </div>
          </div>
        </template>
      </Card>
    </div>
  </template>
  

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Dropdown from 'primevue/dropdown';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';
import Card from 'primevue/card';

const router = useRouter();

// Form fields
const name = ref('');
const breed = ref('');
const age = ref(null);
const sex = ref('');
const history = ref('');
const description = ref('');
const photo = ref(null);

// Options for the sex dropdown
const sexOptions = [
  { label: 'Male' },
  { label: 'Female' }
];

// Handle create animal logic
const handleCreateAnimal = async () => {
  try {
    const animalData = {
      name: name.value,
      breed: breed.value,
      age: age.value,
      sex: sex.value,
      history: history.value,
      description: description.value,
      photo: photo.value  // Assuming file upload handling will process this
    };

    console.log('Animal Data:', animalData);  // Replace with actual API call

    // Reset form fields
    name.value = '';
    breed.value = '';
    age.value = null;
    sex.value = '';
    history.value = '';
    description.value = '';
    photo.value = null;

    alert('Animal created successfully!');
    router.push({ name: 'Home' });  // Redirect after creation
  } catch (error) {
    console.log(error);
    alert('Something went wrong!');
  }
};
</script>

<style scoped>
.sign-up-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  padding: 20px;
}

.title-center {
  text-align: center; /* Center the title */
  font-size: 1.5rem;
}

.input-group {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.input-label {
  width: 90px;
  margin-right: 10px;
  font-size: 1rem;
  text-align: left;
}

.input-text {
  flex-grow: 1;
}

.sign-up-button {
  margin-top: 10px;
}

.w-full {
  width: 100%;
}

.sign-in-text {
  text-align: center;
  margin-top: 10px;
}

.sign-in-redirect button {
  font-size: 1rem;
  margin-left: 5px;
}
</style>
