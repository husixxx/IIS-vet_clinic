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
            /> <!-- feedback=false disables password strength meter -->
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

          <!-- Redirect to Sign Up -->
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

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';  // Import the router for navigation
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import axiosClient from '../api/api';  // Ensure the axiosClient is correctly imported
import { useAuthStore } from '../store/Authstore';  // Ensure correct import of your AuthStore

// Reactive references for the form fields
const username = ref('');
const password = ref('');

// Router and auth store
const router = useRouter();
const authStore = useAuthStore();

// Computed property to validate if the form is valid
const isFormValid = computed(() => {
  return username.value && password.value;  // Both fields must be filled
});

// Sign In handler function
const handleSignIn = async () => {
  try {
    const response = await axiosClient.post(`/authorization/sign_in?username=${username.value}&password=${password.value}`);
    
    // Handle successful login
    const user = {
      username: response.data.username,
      id: response.data.id,
      role_id: response.data.role_id,
    };

    authStore.login(user);  // Save user in Pinia store
    password.value = '';
    username.value = '';
    alert("Login successful");
    router.push({ name: 'Home' });  // Redirect to home after login
  } catch (error) {
    console.log(error);
    alert("Something went wrong");
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
