<template>
  <div class="create-veterinarian-container">
    <Card class="centered-card">
      <template #title">
        <div class="title-center">Create Veterinarian</div>
      </template>
      <template #content>
        <div class="p-fluid">
          <!-- Form inputs -->
          <div class="p-field input-group">
            <label for="first-name" class="input-label">First Name</label>
            <InputText 
              id="first-name" 
              v-model="firstName" 
              placeholder="Enter first name" 
              class="input-text" 
              :class="{'p-invalid': !firstName}" 
            />
          </div>

          <div class="p-field input-group">
            <label for="last-name" class="input-label">Last Name</label>
            <InputText 
              id="last-name" 
              v-model="lastName" 
              placeholder="Enter last name" 
              class="input-text" 
              :class="{'p-invalid': !lastName}"
            />
          </div>

          <div class="p-field input-group">
            <label for="username" class="input-label">Username</label>
            <InputText 
              id="username" 
              v-model="username" 
              placeholder="Enter username" 
              class="input-text" 
              :class="{'p-invalid': !username}"
            />
          </div>

          <div class="p-field input-group">
            <label for="email" class="input-label">Email</label>
            <InputText 
              id="email" 
              v-model="email" 
              placeholder="Enter email" 
              class="input-text" 
              :class="{'p-invalid': !email || !isEmailValid}"  
            />
          </div>

          <div class="p-field input-group">
            <label for="password" class="input-label">Password</label>
            <InputText 
              id="password" 
              type="password" 
              v-model="password" 
              placeholder="Enter password" 
              class="input-text" 
              :class="{'p-invalid': !password}"
            />
          </div>

          <!-- Submit Button -->
          <div class="p-field create-veterinarian-button">
            <Button 
              label="Create Veterinarian" 
              icon="pi pi-check" 
              @click="handleCreateVeterinarian" 
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
import Button from 'primevue/button';
import Card from 'primevue/card';
import axiosClient from '../api/api';  // Ensure correct path to your API client

const router = useRouter();

// Form fields
const username = ref('');
const email = ref('');
const password = ref('');
const firstName = ref('');
const lastName = ref('');

// Regular expression for validating email format
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Computed property to validate if the email format is correct
const isEmailValid = computed(() => emailPattern.test(email.value));

// Form validation (check if all required fields are filled and email is valid)
const isFormValid = computed(() => {
  return firstName.value && lastName.value && username.value && email.value && password.value && isEmailValid.value;
});

// Handle create veterinarian logic
const handleCreateVeterinarian = async () => {
  try {
    // Combine first and last names
    const fullName = `${firstName.value} ${lastName.value}`;

    // Send form data using POST request
    const response = await axiosClient.post(`/admin/veterinarian?username=${username.value}&email=${email.value}&password=${password.value}&name=${fullName}`);

    if (response.status === 201) {
      // Reset form fields
      username.value = '';
      email.value = '';
      password.value = '';
      firstName.value = '';
      lastName.value = '';

      alert('Veterinarian created successfully!');
      router.push({ name: 'Home' });  // Redirect after creation
    }
  } catch (error) {
    console.error('Error creating veterinarian:', error);
    if (error.response && error.response.status === 409) {
      alert('User with this email already exists!');
    } else {
      alert('Failed to create veterinarian.');
    }
  }
};
</script>

<style scoped>
.create-veterinarian-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  padding: 20px;
}

.title-center {
  text-align: center;
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

.create-veterinarian-button {
  margin-top: 10px;
}

.w-full {
  width: 100%;
}

.p-invalid {
  border-color: red;
}
</style>
