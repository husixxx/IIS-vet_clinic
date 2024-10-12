<template>
    <Card>
      <template #content>
        <p class="contact-info">
          <span>Email: vetclinic@gmail.com</span>
          <span>Location: Sered 129/3000, 500</span>
          <span>Tel. number: +421 999 888 777</span>
        </p>
      </template>
    </Card>
  </template>
    
  <script setup>
  import Card from 'primevue/card';  // Import the PrimeVue Card component
  </script>
  
  <style scoped>
  /* Add horizontal spacing between the sections */
  .contact-info span {
    margin-right: 50px;  /* Add spacing between each section */
  }
  
  /* Optional: remove margin for the last item to avoid extra space */
  .contact-info span:last-child {
    margin-right: 0;
  }
  </style>
  