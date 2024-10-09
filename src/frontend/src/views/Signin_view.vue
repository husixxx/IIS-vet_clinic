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
              <Password id="password" v-model="password" placeholder="Enter your password" toggleMask class="input-text" />
            </div>
            
            <!-- Sign In Button -->
            <div class="p-field sign-in-button">
              <Button label="Sign In" icon="pi pi-sign-in" @click="handleSignIn" class="w-full" />
            </div>
          </div>
        </template>
      </Card>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import Card from 'primevue/card';
  import InputText from 'primevue/inputtext';
  import Password from 'primevue/password';
  import Button from 'primevue/button';
  
  const email = ref('');
  const password = ref('');
  
  // Handle sign in logic (mockup for now)
  const handleSignIn = () => {
    console.log('Sign in clicked');
    console.log('Email:', email.value);
    console.log('Password:', password.value);
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
    align-items: center;    /* Vertically center the label and input */
    margin-bottom: 1rem;    /* Reduce the margin for a smaller gap between fields */
  }
  
  .input-label {
    width: 90px;           /* Set a fixed width for the label to align the text */
    margin-right: 10px;     /* Add some space between the label and the input */
    font-size: 1rem;
    text-align: left;       /* Align text in the label to the left */
  }
  
  .input-text {
    flex-grow: 1;           /* Ensure the input takes up the remaining width */
  }
  
  .sign-in-button {
    margin-top: 10px;      /* Add space between the password field and the Sign In button */
  }
  
  .w-full {
    width: 100%;
  }
  </style>
  