<template>
  <div class="content-wrapper">
    <h1 class="welcome-text">Welcome to this page where you can participate in helping animals</h1>
    <h1 class="instruction-text">Click on Sign In to create a volunteer account or to sign into an existing account</h1>
  </div>
</template>

<script setup>
import MyMenubar from '../components/Navbar.vue';  // Importing the Menubar component
</script>

<style scoped>
/* Flexbox container to center the content */
.content-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;    /* Center vertically */
  align-items: center;        /* Center horizontally */
  height: 100vh;              /* Full height of the viewport */
  text-align: center;         /* Center text alignment */
}

/* Styling for the welcome text */
.welcome-text {
  font-size: 2.5rem;       /* Large font size for emphasis */
  font-weight: bold;       /* Bold text */
  color: #4CAF50;          /* Green color to symbolize a welcoming tone */
  margin-bottom: 20px;     /* Add some spacing below */
}

/* Styling for the instruction text */
.instruction-text {
  font-size: 1.5rem;       /* Slightly smaller font for instructions */
  margin-bottom: 30px;     /* Add spacing below */
}
</style>
