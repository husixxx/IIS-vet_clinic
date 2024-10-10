<template>
  <div class="layout-container">
    <!-- Navbar placed at the top (header) -->
    <header>
      <MyMenubar />  <!-- Navbar component -->
    </header>

    <!-- Main content area where routed views are displayed -->
    <main>
      <router-view />  <!-- Inject the page-specific content here -->
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
/* Layout container that uses flexbox to organize header, main, and footer */
.layout-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

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
  flex-grow: 1;
  padding-top: 60px;   /* Space for the header */
  padding-bottom: 60px; /* Space for the footer */
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Footer styling, fixed at the bottom */
footer {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  padding: 10px 0;
  text-align: center;
  z-index: 1000;
}
</style>
