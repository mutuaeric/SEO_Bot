<template>
    <div>
      <h2>Home</h2>
      <SeoForm /> 
    </div>
  </template>
  
  <script>
  import SeoForm from '@/components/SeoForm.vue'; 
  
  export default {
    components: {
      SeoForm
    }
  };
  </script>
  
  <style scoped>
  
  h2 {
    margin-bottom: 20px;
  }
  </style>
  