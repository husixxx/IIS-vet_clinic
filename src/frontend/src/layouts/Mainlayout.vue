<template>
  <div>
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
/* Make the header fixed at the top and ensure it spans the full width */
header {
position: fixed;
top: 0;
left: 0;
width: 100%;
padding: 0;
z-index: 1000;
}

/* Make sure the main content doesn't go behind the fixed header */
main {
margin-top: 30px;  /* Adjust based on the header's height */
}

footer {
   position:fixed;
   left:0px;
   bottom:0px;
   width:100%;
}
</style>