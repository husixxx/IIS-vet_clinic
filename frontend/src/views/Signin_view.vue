<template>
  <div class="sign-in-container">
    <Card>
      <template #title>
        <div class="title-center">Sign in</div>
      </template>
      <template #content>
        <div class="p-fluid">
          <!-- Username Input -->
          <div class="p-field input-group">
            <label for="username" class="input-label">Username</label>
            <InputText 
              id="username" 
              v-model="username" 
              placeholder="Enter your username" 
              class="input-text" 
              :maxlength="30"
            />
          </div>

          <!-- Password Input without feedback -->
          <div class="p-field input-group">
            <label for="password" class="input-label">Password</label>
            <Password 
              id="password" 
              v-model="password" 
              placeholder="Enter your password" 
              toggleMask
              class="input-text" 
              :feedback="false" 
              @input="checkPasswordLength"
            />
          </div>

          <!-- Sign In Button -->
          <div class="p-field sign-in-button">
            <Button 
              label="Sign In" 
              icon="pi pi-sign-in" 
              @click="handleSignIn" 
              class="w-full" 
              :disabled="!isFormValid"
            />
          </div>

          <div class="p-field sign-up-redirect">
            <p class="sign-up-text">Don't have an account yet?
              <Button label="Create one" link @click="redirectToSignUp" />
            </p>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';  // Import the router for navigation
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import axiosClient from '../api/api';  // Ensure the axiosClient is correctly imported
import { useAuthStore } from '../store/Authstore';  // Import the authStore

// Function to ensure password length does not exceed 30 characters
const checkPasswordLength = (event) => {
  if (password.value.length > 30) {
    password.value = password.value.slice(0, 30); // Trim the value to 30 characters
    event.target.value = password.value; // Update the input value to reflect the trimmed value
  }
};

// Reactive references for the form fields
const username = ref('');
const password = ref('');

// Router and auth store
const router = useRouter();
const authStore = useAuthStore();  // Create an instance of the auth store

// Computed property to validate if the form is valid
const isFormValid = computed(() => {
  return username.value && password.value;  // Both fields must be filled
});

// Sign In handler function
const handleSignIn = async () => {
  try {
    const response = await axiosClient.post(
      `/authorization/sign_in?username=${username.value}&password=${password.value}`,
      null,
      { withCredentials: true }
    );

    const userData = response.data[0]; 

    // Map response data to the user object
    const user = {
      username: userData.username,
      id: userData.id,
      role_id: userData.role_id,
    };

    authStore.login(user); // Login with the mapped user object
    password.value = '';
    username.value = '';
    router.push({ name: 'Home' }); // Redirect to home after login
  } 
  catch (error) {
  if (error.response) {

    const status = error.response.status;
    const error_msg = error.response.data.error;
    console.error(`Error Status: ${status}`);
    alert(error_msg);
  } else {

    console.error("Error:", error.message);
    alert("Something went wrong. Please try again later.");
  }
}
};

// Redirect to sign up page
const redirectToSignUp = () => {
  router.push({ name: 'Signup' });
};
</script>

<style scoped>

.w-full {
  width: 100%;
}

.title-center {
  text-align: center;
  padding-bottom: 10px;
}

</style>
