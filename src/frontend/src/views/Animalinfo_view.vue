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
  // Zatiaľ žiadna špecifická logika, toto je len statický layout
  </script>
  
  <style scoped>
  .main-content {
    display: grid;
    grid-template-columns: 1.5fr 2.5fr;  /* Make medical records and schedule wider */
    grid-template-rows: auto auto;     /* Allow the rows to adjust based on content */
    gap: 20px;                         /* Medzi jednotlivými sekciami bude medzera */
    padding: 20px;
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
  