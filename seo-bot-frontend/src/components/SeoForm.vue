<template>
  <div class="seo-form">
    <h2>SEO Form</h2>
    <div class="form-group">
      <label for="urlInput">Enter Website URL:</label>
      <input id="urlInput" v-model="url" placeholder="https://example.com" />
    </div>
    
    <div class="form-group">
      <button class="btn-submit" @click="checkBrokenLinks" :disabled="loadingCheck">
        <span v-if="loadingCheck">
          <i class="fas fa-circle-notch fa-spin"></i> Loading...
        </span>
        <span v-else>
          Check Broken Links
        </span>
      </button>
    </div>
    
    <div class="form-group">
      <input type="file" @change="handleFileUpload" />
      <button class="btn-submit" @click="analyzeSpreadsheet" :disabled="loadingAnalyze">
        <span v-if="loadingAnalyze">
          <i class="fas fa-circle-notch fa-spin"></i> Loading...
        </span>
        <span v-else>
          Analyze Spreadsheet
        </span>
      </button>
    </div>

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
      results: null,
      error: null,
      loadingCheck: false,
      loadingAnalyze: false
    };
  },
  methods: {
    checkBrokenLinks() {
      this.loadingCheck = true;  // Set loading state for checkBrokenLinks

      let encodedUrl = encodeURIComponent(this.url);
      axios
        .get(`http://localhost:8000/api/seo/check-broken-links/?url=${encodedUrl}`)
        .then(response => {
          console.log('Response:', response.data);
          this.results = response.data;
          this.error = null;
        })
        .catch(error => {
          console.error('Error checking broken links:', error);
          this.error = 'Failed to check broken links';
          this.results = null;
        })
        .finally(() => {
          this.loadingCheck = false;  // Reset loading state for checkBrokenLinks
        });
    },
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    analyzeSpreadsheet() {
      this.loadingAnalyze = true;  // Set loading state for analyzeSpreadsheet

      let formData = new FormData();
      formData.append('file', this.file);

      axios
        .post(`http://localhost:8000/api/seo/analyze-spreadsheet/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          console.log('Response:', response.data);
          this.results = response.data;
          this.error = null;
        })
        .catch(error => {
          console.error('Error analyzing spreadsheet:', error);
          this.error = 'Failed to analyze spreadsheet';
          this.results = null;
        })
        .finally(() => {
          this.loadingAnalyze = false;  // Reset loading state for analyzeSpreadsheet
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
  max-width: 800px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 80%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
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
  margin-top: 5px;
  position: relative;
}

.btn-submit span {
  display: inline-block;
}

.btn-submit i {
  margin-right: 5px;
}

.btn-submit:hover {
  background-color: #85c961;
}

.fa-spin {
  animation: spin 1s infinite linear;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
