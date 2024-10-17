<template>
  <div class="main-content">
    <!-- Div pre fotku -->
    <div class="photo-section">
      <img src="https://via.placeholder.com/300" alt="Animal photo" />
    </div>

    <!-- Div pre popis (description) -->
    <div class="description-section">
      <h3>Name</h3>
      <p>Breed</p>
      <p>Location of funding</p>
      <p>Age</p>
      <p>Description</p>
    </div>

    <!-- Div pre zdravotné záznamy (medical records) -->
    <div class="medical-records-section">
      <h3>Medical records</h3>
      <p>Details about the medical history of the animal.</p>
    </div>

    <!-- Div pre rezervácie (schedule) -->
    <div class="schedule-section">
      <h3>Schedule</h3>
      <p>11.8.2024</p>
    </div>
  </div>
</template>
  
<script setup>

import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axiosClient from '../api/api';
import { useAuthStore } from '../store/Authstore';  // Ensure correct import of your AuthStore

const authStore = useAuthStore();
const user = authStore.getUser;
const userRole = authStore.getRoleId;

const router = useRoute();

onMounted(async () => {
  try {
    const response = await axiosClient.get(`/animal/info?animal_id=${encodeURIComponent(router.params.id)}`);
    console.log(response.data);
    // animals.value = response.data;  // Assign the array of animals
    // console.log(animals.value);
  } catch (error) {
    console.error('Error fetching animal data:', error);
  }
});

</script>
  
<style scoped>

.main-content {
  display: grid;
  grid-template-columns: 0.8fr 2.5fr;  /* Make medical records and schedule wider */
  gap: 20px;                         /* Medzi jednotlivými sekciami bude medzera */
  padding: 20px;
  margin-bottom: 115;
}

/* Styling for each section */
.photo-section img {
  width: 100%;
  height: auto;
  object-fit: cover;
  border-radius: 10px;
}

.description-section, .medical-records-section, .schedule-section {
  background-color: #f0f0f0;
  padding: 15px;  /* Reduced padding to reduce height */
  border-radius: 10px;
}

.description-section {
  grid-row: 2 / span 1;  /* Description sekcia bude v druhom riadku */
}

.medical-records-section {
  grid-column: 2 / span 1;  /* Bude na pravej strane vedľa fotky */
  grid-row: 1 / span 1;
}

.schedule-section {
  grid-column: 2 / span 1;
  grid-row: 2 / span 1;
}

</style>
  