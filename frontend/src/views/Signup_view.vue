<template>
  <div class="sign-up-container">
    <Card>
      <template #title>Sign Up</template>
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

          <!-- Phone Number Input -->
          <div class="p-field input-group">
            <label for="phone" class="input-label">Phone</label>
            <InputText id="phone" type="tel" v-model="phone" placeholder="Enter your phone number" class="input-text" />
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
import { ref } from 'vue';
import { useRouter } from 'vue-router';  // Import the router for navigation
import Card from 'primevue/card';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';

const firstName = ref('');
const lastName = ref('');
const phone = ref('');
const email = ref('');
const password = ref('');

// Using router to navigate
const router = useRouter();

// Handle sign up logic (mockup for now)
const handleSignUp = () => {
  console.log('Sign up clicked');
  console.log('First Name:', firstName.value);
  console.log('Last Name:', lastName.value);
  console.log('Phone:', phone.value);
  console.log('Email:', email.value);
  console.log('Password:', password.value);
};

// Redirect to Sign In using named route
const redirectToSignIn = () => {
  router.push({ name: 'Sign' });  // Use the named route 'Sign' for Sign In
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