<template>
  <div class="sign-up-container">
    <Card>
      <template #title>
        <div class="title-center">Sign up</div>
      </template>
      <template #content>
        <div class="p-fluid">
          <!-- First Name Input -->
          <div class="p-field input-group">
            <label for="firstName" class="input-label">First Name</label>
            <InputText id="firstName" v-model="firstName" placeholder="Enter your first name" class="input-text" />
          </div>

          <!-- Last Name Input -->
          <div class="p-field input-group">
            <label for="lastName" class="input-label">Last Name</label>
            <InputText id="lastName" v-model="lastName" placeholder="Enter your last name" class="input-text" />
          </div>

          <!-- Username Input -->
          <div class="p-field input-group">
            <label for="username" class="input-label">Username</label>
            <InputText id="username" v-model="username" placeholder="Enter your username" class="input-text" />
          </div>

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

          <!-- Sign Up Button -->
          <div class="p-field sign-up-button">
            <Button label="Sign Up" icon="pi pi-user-plus" @click="handleSignUp" class="w-full" />
          </div>

          <!-- Redirect to Sign In -->
          <div class="p-field sign-in-redirect">
            <p class="sign-in-text">Already have an account?
              <Button label="Sign In" link @click="redirectToSignIn" />
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

const firstName = ref('');
const lastName = ref('');
const username = ref('');
const email = ref('');
const password = ref('');

// Combine first name and last name into one string
const fullName = computed(() => `${firstName.value} ${lastName.value}`);

// Using router to navigate
const router = useRouter();

const handleSignUp = async () => 
{
  try 
  {
    const response = await axiosClient.post(`/authorization/sign_up?username=${username.value}&email=${email.value}&password=${password.value}&name=${fullName.value}`);

    // Reset form fields after successful sign-up
    firstName.value = '';
    lastName.value = '';
    username.value = '';
    email.value = '';
    password.value = '';

    alert("Your volunteer account has to be approved by caretaker");
  } 
  catch (error) 
  {
    // handle error
    console.log(error);
    alert("Something went wrong");
  }
};

// Redirect to Sign In using named route
const redirectToSignIn = () => {
  router.push({ name: 'Sign' });  // Use the named route 'Sign' for Sign In
};
</script>

<style scoped>

.w-full {
  width: 100%;
}

.title-center{
  text-align: center;
  padding-bottom: 10px;
}

</style>
