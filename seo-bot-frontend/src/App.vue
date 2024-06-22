<template>
  <div id="app">
    <header>
      <h1>SEO Bot</h1>
      <nav>
       
      </nav>
    </header>
    
    <main>
      <router-view />
    </main>
    
    <footer>
      <p>&copy; 2024 Your Company</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {
    
  }
};
</script>

<style scoped>

body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

header {
  background-color: #f0f0f0;
  padding: 10px;
  text-align: center;
}

nav {
  margin-top: 10px;
}

main {
  margin: 20px;
}

footer {
  background-color: #333;
  color: #fff;
  text-align: center;
  padding: 10px;
  position: fixed;
  bottom: 0;
  width: 100%;
}
</style>
