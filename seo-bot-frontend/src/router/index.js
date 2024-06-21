import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';

const routes = [
  { path: '/', component: HomePage },
  // Add more routes as needed for other views/components
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
