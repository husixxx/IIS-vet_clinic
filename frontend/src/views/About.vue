<template>
    <div class="about-us">
      <!-- What We Do Section -->
      <Fieldset legend="What We Do">
        <p class="m-0">
          We provide a loving environment for abandoned animals such as rabbits, cats, dogs, and more. Our mission is to help these animals find care and a temporary home through volunteers who can walk and care for them.
        </p>
      </Fieldset>
  
      <!-- Animal Information Section -->
      <Fieldset legend="Animal Information">
        <p class="m-0">
          Each animal is identified by their name, species, and various attributes like age, photos, and more. Our system maintains detailed information on each animal’s history, including how they were found, their medical condition, vaccinations, and veterinary check-ups.
        </p>
      </Fieldset>
  
      <!-- Volunteer Opportunities Section -->
      <Fieldset legend="Volunteer Opportunities">
        <p class="m-0">
          Verified volunteers can search for animals in need and make reservations to walk them based on available slots. Our system ensures a structured and easy process for volunteers to participate and contribute to the well-being of these animals.
        </p>
      </Fieldset>
  
      <!-- Join Our Mission Section -->
      <Fieldset legend="Join Our Mission">
        <p class="m-0">
          Through this system, we aim to ensure that every animal receives the care they deserve, while giving volunteers a chance to make a difference. Join us in our mission to give these animals a better life.
        </p>
      </Fieldset>
    </div>
  </template>
  
  <script setup>
  import Fieldset from 'primevue/fieldset';  // Import the Fieldset component
  </script>
  
<style scoped>

.about-us {
  display: flex;
  flex-direction: column;
  align-items: center;  /* Center the fieldsets horizontally */
  margin-bottom: 120px;
  margin-left: 50px;
  margin-right: 50px;
}

fieldset {
  width: 100%;              /* Ensure fieldset takes full width of the container */
  max-width: 800px;          /* Set a maximum width to limit stretching on large screens */
  margin-bottom: 20px;       /* Add spacing between fieldsets */
}

p {
  text-align: justify;       /* Optional: Makes text justify for a neat appearance */
  line-height: 1.6;          /* Add some line spacing for better readability */
}
</style>
  