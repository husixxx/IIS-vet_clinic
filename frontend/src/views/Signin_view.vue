<template>
  <div class="sign-in-container">
    <Card>
      <template #title>Sign In</template>
      <template #content>
        <div class="p-fluid">
          <!-- Email Input -->
          <div class="p-field input-group">
            <label for="email" class="input-label">Email</label>
            <InputText id="email" type="email" v-model="email" placeholder="Enter your email" class="input-text" />
          </div>

          <!-- Password Input -->
          <div class="p-field input-group">
            <label for="password" class="input-label">Password</label>
            <Password id="password" v-model="password" placeholder="Enter your password" toggleMask
              class="input-text" />
          </div>

          <!-- Sign In Button -->
          <div class="p-field sign-in-button">
            <Button label="Sign In" icon="pi pi-sign-in" @click="handleSignIn" class="w-full" />
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
import { ref } from 'vue';
import { useRouter } from 'vue-router';  // Import the router for navigation
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
// import apiClient from '../api';
import axiosClient from '../api/api';

const email = ref('');
const password = ref('');

// Using router to navigate
const router = useRouter();

// Handle sign in logic (mockup for now)
const handleSignIn = async () => {
  
  axiosClient.post('/authorization/sign_in')
  .then((res) => { 
    email.value = res.data.email
  })
};

// Redirect to Sign Up using named route
const redirectToSignUp = () => {
  router.push({ name: 'Signup' });  // Use the named route 'Signup'
};

</script>

<style scoped>
.sign-in-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80vh;
  padding: 20px;
}

/* Flexbox to align labels and inputs properly */
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

.sign-in-button {
  margin-top: 10px;
}

.w-full {
  width: 100%;
}

.sign-up-text {
  text-align: center;
  margin-top: 10px;
}

.sign-up-redirect button {
  font-size: 1rem;
  margin-left: 5px;
}
</style>
