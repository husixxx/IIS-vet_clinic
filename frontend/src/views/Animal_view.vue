<template>
  <div>
    <h1 id="main-title">Animals in our shelter</h1>
    <div id="boxes">
      <div id="leftbox">
        <FilterPanel @filter-animals="handleFilter" />
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
import { ref } from 'vue';
import axiosClient from '../api/api';
import FilterPanel from '../components/Sidepanel.vue';
import Animalcard from '../components/Animalcard.vue';

const animals = ref([]);

// Function to fetch animals with filters
const fetchAnimals = async (filters = {}) => {
  try {
    console.log('Fetching with filters:', filters);  // Debug to check filters in fetchAnimals
    const response = await axiosClient.get('/filter_animals', { params: filters });
    animals.value = response.data;  // Update the animal list
  } catch (error) {
    console.error('Error fetching animal data:', error);
  }
};

// Handle the event emitted from FilterPanel
const handleFilter = (filters) => {
  fetchAnimals(filters);  // Fetch filtered animals
};

// Fetch all animals initially
fetchAnimals();
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
