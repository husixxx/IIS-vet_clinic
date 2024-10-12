<template>
  <div>
    <h1 id="main-title">GeeksforGeeks</h1> <!-- Center the title above the boxes -->
    <div id="boxes">
      <div id="leftbox">
        <FilterPanel />
      </div>
      <div id="cards">
        <card v-for="n in numberOfCards" :key="n"/>
      </div>
    </div>
  </div>
</template>

<script setup>
import FilterPanel from '../components/Sidepanel.vue'; // Adjust path if necessary
import card from '../components/Animalcard.vue'; // Adjust path if necessary

const numberOfCards = 5; // Adjust number based on your requirement or dynamic data
</script>

<style scoped>
#main-title {
  text-align: center;
  margin-bottom: 20px;
}

#boxes {
  display: flex;
  align-items: flex-start; /* Align items at the start of the flex container */
}

#leftbox {
  width: 25%; /* Adjust width as needed */
  min-width: 200px; /* Minimum width to ensure usability */
}

#cards {
  display: flex;
  flex-wrap: wrap; /* Allows cards to wrap onto the next line */
  gap: 10px; /* Spacing between cards */
}

card {
  flex: 1 0 120px; /* Each card can grow but starts with 120px base width */
  height: 200px; /* Adjust height as necessary */
  background-color: lightgrey; /* Example color, adjust as necessary */
}
</style>
