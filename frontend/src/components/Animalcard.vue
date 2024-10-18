<template>
  <Card
    style="width: 25rem; overflow: hidden; cursor: pointer"
    @click="handleCardClick"
    class="hover-card"
  >
    <!-- Photo section -->
    <template #header>
      <div v-if="animalPhoto" class="image-wrapper">
        <img :src="animalPhoto" alt="Animal Photo" />
      </div>
      <div v-else class="image-placeholder"></div>
    </template>

    <!-- Name, Breed, and Age -->
    <template #title>{{ name }}</template>
    <template #content>
      <p class="m-0">
        <span class="breed">Breed: {{ breed }}</span><br />
        <span class="age">Age: {{ age }}</span>
      </p>
      <!-- Add padding before description -->
      <p class="description">{{ description }}</p>
    </template>
  </Card>
</template>

<script setup>
import { computed } from 'vue';
import Card from 'primevue/card';

// Props passed to the card
const props = defineProps({
  name: String,
  breed: String,
  age: Number,
  photo: String,
  description: String,
});

// Handle photo (convert it to a URL or leave empty if no photo is available)
const animalPhoto = computed(() => {
  if (props.photo) {
    return `data:image/jpeg;base64,${props.photo}`;  // Base64-encoded image
  }
  return null;
});

// Handle the card click
const handleCardClick = () => {
  // You can redirect to another page or handle any action here
  alert(`You clicked on ${props.name}`);
};
</script>

<style scoped>
.image-wrapper {
  width: 100%;
  height: 150px;
  background-color: #f0f0f055;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 150px;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.breed {
  color: #aaa;
}

.age {
  color: #aaa;
}

.description {
  margin-top: 10px;
  white-space: normal;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.hover-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-10px);
  box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.1);
}
</style>
