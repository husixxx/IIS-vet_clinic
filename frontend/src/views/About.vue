<template>
    <div class="about-us">
      <!-- What We Do Section -->
      <Fieldset legend="Caring for Abandoned Dogs">
        <p class="m-0">
          At our shelter, we are committed to giving abandoned and stray dogs a second chance at life. Every dog that comes through our doors is treated with love and compassion, ensuring they receive the care they need to heal, both physically and emotionally.
        </p>
      </Fieldset>
  
      <!-- Animal Information Section -->
      <Fieldset legend="Comprehensive Care and Well-being">
        <p class="m-0">
          We provide a safe environment where every dog has access to proper nutrition, medical attention, and socialization. From regular veterinary check-ups to personalized care plans, we make it our mission to prioritize their well-being.
        </p>
      </Fieldset>
  
      <!-- Volunteer Opportunities Section -->
      <Fieldset legend="Volunteer-Led Dog Walking Program">
        <p class="m-0">
          Our verified volunteers play a vital role in enriching the lives of our dogs. Through our structured dog-walking program, volunteers give the dogs the physical exercise, attention, and companionship they need to stay happy and healthy.
        </p>
      </Fieldset>
  
      <!-- Join Our Mission Section -->
      <Fieldset legend="Building a Community of Care">
        <p class="m-0">
          We are more than just a shelter – we are a community. Our team of caretakers, veterinarians, and volunteers work together to ensure every dog has a bright future. By fostering this connection, we create a network of support for both the animals and the people who care for them.
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
  