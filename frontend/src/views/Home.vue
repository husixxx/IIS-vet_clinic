<template>
  <div class="content-wrapper">
    <h1 class="welcome-text">Welcome to this page where you can participate in helping animals</h1>
    <h2 class="instruction-text">Click on Sign In to create a volunteer account or to sign into an existing account</h2>
  </div>
</template>

<style scoped>

.content-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  text-align: center;
}

.welcome-text {
  font-size: 2.5rem; /* Large font size for the welcome message */
  font-weight: bold; /* Bold font for emphasis */
  margin-bottom: 20px; /* Space between the welcome and instruction text */
  opacity: 0.9; /* Slightly see-through */
}

.instruction-text {
  font-size: 1.5rem; /* Appropriate font size for secondary information */
  font-weight: 300; /* Lighter font for less emphasis */
  letter-spacing: 1px; /* Space out the letters a bit for better readability */
  opacity: 0.85; /* Slightly see-through */
}
</style>
