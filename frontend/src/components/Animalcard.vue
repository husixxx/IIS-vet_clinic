<template>
    <Card style="width: 25rem; overflow: hidden">
        <template #title>{{ name }}</template>
        <template #subtitle>Breed: {{ breed }}</template>
        <template #content>
            <p class="m-0">
                Age: {{ age }}<br />
                {{ description }}
            </p>
        </template>
        <template #footer>
            <div class="flex justify-center">
                <Button label="Info" class="w-full" />
            </div>
        </template>
    </Card>
</template>

<script setup>
import Card from 'primevue/card';
import Button from 'primevue/button';

// Props passed to the card
const props = defineProps({
  name: String,
  breed: String,
  age: Number,
  description: String,
});
</script>

<style scoped>
/* Optional: Add custom styles here */
</style>
