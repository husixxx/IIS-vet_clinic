<template>
  <div class="layout-container">
    <!-- Navbar placed at the top (header) -->
    <header>
      <MyMenubar /> <!-- Navbar component -->
    </header>

    <!-- Main content area where routed views are displayed -->
    <main>
      <router-view /> <!-- Inject the page-specific content here -->
    </main>

    <!-- Optional footer -->
    <footer>
      <Footer />
    </footer>
  </div>
</template>

<script setup>
import MyMenubar from '../components/Navbar.vue';
import Footer from '../components/Footer.vue';
</script>

<style scoped>

/* Header styling, fixed at the top */
header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  padding: 0;
}

/* Main content styling, flex-grow ensures it takes up available space */
main {
  padding-top: 100px; /* Space for the header */
  padding-bottom: 100px; /* Space for the footer */
  width: 100%; /* Ensure main takes up full width */
  flex-grow: 1; /* Ensures the main content takes available space */
  color: white; /* Ensure the text is visible */
}

/* Footer styling, fixed at the bottom */
footer {
  position: fixed; /* Optional: only if you want the footer fixed like the navbar */
  bottom: 0; /* Aligns it at the bottom */
  left: 0; /* Aligns it to the left edge of the viewport */
  width: 100%; /* Ensures it takes up the full viewport width */
  color: white; /* Ensuring text is visible */
  text-align: center; /* Center the text inside the footer */
  z-index: 1000; /* Ensures it stays on top of other content if overlapping occurs */
  --p-card-border-radius: 0px;
}
</style>
