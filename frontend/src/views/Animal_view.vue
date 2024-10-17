<template>
  <div>
    <h1 id="main-title">Animal Information</h1>
    <div id="boxes">
      <div id="leftbox">
        <FilterPanel />
      </div>
      <div id="cards">
        <Animalcard
          v-for="animal in animals"
          :key="animal.id"
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

// Fetch all animal data from backend
onMounted(async () => {
  try {
    const response = await axiosClient.get('/animal/info');
    animals.value = response.data;
    console.log(animals.value);
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
  align-items: flex-start;
}

#leftbox {
  width: 25%;
  min-width: 200px;
}

#cards {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 115px;
}

Animalcard {
  flex: 1 0 120px;
  height: auto;
  background-color: lightgrey;
}
</style>
