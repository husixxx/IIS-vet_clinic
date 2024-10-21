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
            <InputText 
              id="name" 
              v-model="name" 
              placeholder="Enter the animal's name" 
              class="input-text" 
              :class="{'p-invalid': !name}" 
            />
          </div>

          <div class="p-field input-group">
            <label for="breed" class="input-label">Breed</label>
            <InputText 
              id="breed" 
              v-model="breed" 
              placeholder="Enter the breed" 
              class="input-text" 
              :class="{'p-invalid': !breed}" 
            />
          </div>

          <div class="p-field input-group">
            <label for="age" class="input-label">Age</label>
            <InputNumber 
              id="age" 
              v-model="age" 
              placeholder="Enter the age" 
              class="input-text" 
              :class="{'p-invalid': !age}" 
            />
          </div>

          <div class="p-field input-group">
            <label for="sex" class="input-label">Sex</label>
            <Dropdown
              v-model="sex"
              :options="sexOptions"
              optionLabel="label"
              optionValue="value"
              placeholder="Select sex"
              class="input-text"
              :class="{'p-invalid': !sex}" 
            />
          </div>

          <!-- File Upload for Animal Photo (optional) -->
          <div class="p-field input-group">
            <label for="photo" class="input-label">Photo</label>
            <input
              type="file"
              @change="handleFileUpload"
              accept="image/*"
              class="file-input"
            />
          </div>

          <!-- History (optional) -->
          <div class="p-field input-group">
            <label for="history" class="input-label">History</label>
            <Textarea id="history" v-model="history" placeholder="Enter animal's history" class="input-text" rows="5" />
          </div>

          <!-- Description (optional) -->
          <div class="p-field input-group">
            <label for="description" class="input-label">Description</label>
            <Textarea id="description" v-model="description" placeholder="Enter description" class="input-text" rows="5" />
          </div>

          <!-- Submit Button -->
          <div class="p-field sign-up-button">
            <Button 
              label="Create Animal" 
              icon="pi pi-check" 
              @click="handleCreateAnimal" 
              class="w-full" 
              :disabled="!isFormValid"
            />
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import Dropdown from 'primevue/dropdown';
import Textarea from 'primevue/textarea';
import Button from 'primevue/button';
import Card from 'primevue/card';
import axiosClient from '../api/api';  // Ensure correct path to your API client

const router = useRouter();

// Form fields
const name = ref('');
const breed = ref('');
const age = ref(null);
const sex = ref('');
const history = ref('');
const description = ref('');
const photoFile = ref(null);  // To store the uploaded photo file

// Options for the sex dropdown
const sexOptions = [
  { label: 'Male', value: 'Male' },
  { label: 'Female', value: 'Female' }
];

// Handle file upload
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    photoFile.value = file;  // Store the file
  }
};

// Form validation (check if required fields are filled)
const isFormValid = computed(() => {
  return name.value && breed.value && age.value && sex.value;  // Only required fields are checked
});

// Handle create animal logic
const handleCreateAnimal = async () => {
  try {
    // Prepare form data with the animal details
    const formData = new FormData();
    formData.append('name', name.value);
    formData.append('breed', breed.value);
    formData.append('age', age.value);
    formData.append('sex', sex.value);
    formData.append('history', history.value);
    formData.append('description', description.value);
    
    // Append the photo file if available
    if (photoFile.value) {
      formData.append('photo', photoFile.value);
    }

    // Send form data using POST request
    const response = await axiosClient.post('/caretaker/animal', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    if (response.status === 201) {
      // Reset form fields
      name.value = '';
      breed.value = '';
      age.value = null;
      sex.value = '';
      history.value = '';
      description.value = '';
      photoFile.value = null;

      alert('Animal created successfully!');
      router.push({ name: 'Home' });  // Redirect after creation
    }
  } catch (error) {
    console.error('Error creating animal:', error);
    alert('Failed to create animal.');
  }
};
</script>

<style scoped>
.title-center {
  text-align: center;
  font-size: 1.5rem;
}

.w-full {
  width: 100%;
}

.file-input {
  width: 73%;
  padding: 8px;
  padding-left: 5px;
  border: 1px solid #333333;
  background-color: #09090b;
  color: #a1a1aa;
  border-radius: 4px;
}

.p-invalid {
  border-color: red;
}
</style>
