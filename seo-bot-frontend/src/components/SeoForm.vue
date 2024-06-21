<template>
  <div class="seo-form">
    <h2>SEO Form</h2>
    <div class="form-group">
      <label for="urlInput">Enter Website URL:</label>
      <input id="urlInput" v-model="url" placeholder="https://example.com" />
    </div>
    
    <button class="btn-submit" @click="checkBrokenLinks">Check Broken Links</button>
    
    <input type="file" @change="handleFileUpload" />
    <button class="btn-submit" @click="analyzeSpreadsheet">Analyze Spreadsheet</button>

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
        .get(`http://localhost:8000/api/seo/check-broken-links/?url=${this.url}`)
        .then(response => {
          this.results = response.data;
        })
        .catch(error => {
          console.error('Error checking broken links:', error);
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
          console.error('Error analyzing spreadsheet:', error);
        });
    }
  }
};
</script>

<style scoped>
.seo-form {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.btn-submit {
  background-color: #a3d977;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 3px;
  transition: background-color 0.3s ease;
  margin-right: 10px;
}

.btn-submit:hover {
  background-color: #85c961;
}
</style>
