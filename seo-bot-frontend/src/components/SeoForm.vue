<template>
  <div>
    <h2>SEO Bot</h2>
    <input v-model="url" placeholder="Enter website URL" />
    <button @click="checkBrokenLinks">Check Broken Links</button>
    <input type="file" @change="handleFileUpload" />
    <button @click="analyzeSpreadsheet">Analyze Spreadsheet</button>
    <div v-if="results">
      <h3>Results</h3>
      <pre>{{ results }}</pre>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      url: '',
      file: null,
      results: null
    };
  },
  methods: {
    checkBrokenLinks() {
      axios
        .get(`http://localhost:8000/api/seo/check-broken-links/`, {
          params: { url: this.url }
        })
        .then(response => {
          this.results = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    analyzeSpreadsheet() {
      let formData = new FormData();
      formData.append('file', this.file);

      axios
        .post(`http://localhost:8000/api/seo/analyze-spreadsheet/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          this.results = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
};
</script>
