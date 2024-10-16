<template>
    <div class="create-caretaker-container">
      <Card class="centered-card">
        <template #title">
          <div class="title-center">Create Caretaker</div>
        </template>
        <template #content>
          <div class="p-fluid">
            <!-- Form inputs -->
            <div class="p-field input-group">
              <label for="first-name" class="input-label">First Name</label>
              <InputText id="first-name" v-model="firstName" placeholder="Enter first name" class="input-text" />
            </div>
  
            <div class="p-field input-group">
              <label for="last-name" class="input-label">Last Name</label>
              <InputText id="last-name" v-model="lastName" placeholder="Enter last name" class="input-text" />
            </div>
            
            <div class="p-field input-group">
              <label for="username" class="input-label">Username</label>
              <InputText id="username" v-model="username" placeholder="Enter username" class="input-text" />
            </div>
  
            <div class="p-field input-group">
              <label for="email" class="input-label">Email</label>
              <InputText id="email" v-model="email" placeholder="Enter email" class="input-text" />
            </div>
  
            <div class="p-field input-group">
              <label for="password" class="input-label">Password</label>
              <InputText id="password" type="password" v-model="password" placeholder="Enter password" class="input-text" />
            </div>
  
  
            <!-- Submit Button -->
            <div class="p-field create-caretaker-button">
              <Button label="Create Caretaker" icon="pi pi-check" @click="handleCreateCaretaker" class="w-full" />
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
  
  // Handle create caretaker logic
  const handleCreateCaretaker = async () => {
    try {
      // Combine first and last names
      const fullName = `${firstName.value} ${lastName.value}`;
  
      // Send form data using POST request
      const response = await axiosClient.post(`/admin/caretaker?username=${username.value}&email=${email.value}&password=${password.value}&name=${fullName}`);
  
      if (response.status === 201) {
        // Reset form fields
        username.value = '';
        email.value = '';
        password.value = '';
        firstName.value = '';
        lastName.value = '';
  
        alert('Caretaker created successfully!');
        router.push({ name: 'Home' });  // Redirect after creation
      }
    } catch (error) {
      console.error('Error creating caretaker:', error);
      if (error.response && error.response.status === 409) {
        alert('User with this email already exists!');
      } else {
        alert('Failed to create caretaker.');
      }
    }
  };
  </script>
  
  <style scoped>
  .create-caretaker-container {
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
  
  .create-caretaker-button {
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
  