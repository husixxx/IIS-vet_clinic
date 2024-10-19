<template>
  <div>
    <h1 id="main-title">Animals in our shelter</h1>
    <div id="boxes">
      <div id="leftbox">
        <FilterPanel />
      </div>
      <div id="cards">
        <Animalcard
          v-for="animal in animals"
          :key="animal.name"
          :name="animal.name"
          :breed="animal.breed"
          :age="animal.age"
          :photo="animal.photo" 
          :description="animal.description"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axiosClient from '../api/api';
import FilterPanel from '../components/Sidepanel.vue';
import Animalcard from '../components/Animalcard.vue';

const animals = ref([]);

// Fetch all animal data from the backend
onMounted(async () => {
  try {
    const response = await axiosClient.get('/caretaker/animals');
    animals.value = response.data;  // Assign the array of animals
  } catch (error) {
    console.error('Error fetching animal data:', error);
  }
});
</script>

<style scoped>
#main-title {
  text-align: center;
  margin-bottom: 20px;
}

#boxes {
  display: flex;
  justify-content: space-between; /* Ensures even spacing between side panel and cards */
  align-items: flex-start;
  margin-left: 20px; /* Space from the left edge */
  margin-right: 20px; /* Space from the right edge */
}

#leftbox {
  width: 25%;
  min-width: 200px;
}

#cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* Ensures 4 cards per row */
  gap: 10px;
  margin-bottom: 115px;
}

#Animalcard {
  height: auto;
  background-color: lightgrey;
}
</style>
