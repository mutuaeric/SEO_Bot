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
    
    <!-- Upload Excel File -->
   <!--  <div class="form-group">
      <label for="fileInput">Upload Spreadsheet (Excel or CSV):</label>
      <input type="file" id="fileInput" @change="handleFileUpload" />
      <button class="btn-submit" @click="analyzeSpreadsheet" :disabled="loadingAnalyze">
        <span v-if="loadingAnalyze">
          <i class="fas fa-circle-notch fa-spin"></i> Analyzing...
        </span>
        <span v-else>
          Extract Links from Spreadsheet
        </span>
      </button>
    </div> 

    !-- Extracted Links Section --

    <div v-if="error" class="error">{{ error }}</div>
    <table v-if="extractedLinks.length > 0">
      <thead>
        <tr>
          <th>Link</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(link, index) in extractedLinks" :key="index">
          <td>{{ link }}</td>
        </tr>
      </tbody>
    </table> 

    <div v-if="loadingAnalyze">Analyzing spreadsheet...</div> -->
  </div> 
     <!-- Results Section -->
     <div v-if="results">
      <h3>Results</h3>
      <table class="results-table">
        <thead>
          <tr>
            <th>Category</th>
            <th>Details</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(value, key) in results" :key="key">
            <td>{{ key }}</td>
            <td>
              <ul v-if="Array.isArray(value)">
                <li v-for="(item, index) in value" :key="index">{{ item }}</li>
              </ul>
              <span v-else>{{ value }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Error Handling -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      url: '',
      file: null,
      extractedLinks: [],
      results: null,
      error: null,
      loadingAnalyze: false,
      loadingCheck: false,
      loadingCheckAll: false
    };
  },
  methods: {
    checkBrokenLinks() {
      if (!this.url) {
        this.error = 'Please enter a valid URL';
        return;
      }
      this.loadingCheck = true;

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
          this.loadingCheck = false;
        });
    },
   /*  handleFileUpload(event) {
      this.file = event.target.files[0];
      console.log('Uploaded file:', this.file);
    },
    
    analyzeSpreadsheet() {
      if (!this.file) {
        this.error = 'Please upload a spreadsheet file';
        return;
      }

      this.loadingAnalyze = true;
      let formData = new FormData();
      formData.append('file', this.file);

      axios
        .post(`http://localhost:8000/api/seo/analyze-spreadsheet/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          console.log('Response from analyze spreadsheet:', response.data);
          this.extractedLinks = response.data.links || [];
          this.error = this.extractedLinks.length > 0 ? null : 'No links found in the spreadsheet';
        })
        .catch(error => {
          console.error('Error extracting links from spreadsheet:', error);
          this.error = 'Failed to extract links from spreadsheet';
          this.extractedLinks = [];
        })
        .finally(() => {
          this.loadingAnalyze = false;
        });
    },

    checkAllBrokenLinks() {
      
      if (this.extractedLinks.length === 0) {
        this.error = 'No links to check';
        return;
      }

      this.loadingCheckAll = true;

      // Assume you have an API endpoint to check all broken links in one go
      axios
        .post(`http://localhost:8000/api/seo/check-all-broken-links/`, {
          links: this.extractedLinks
        })
        .then(response => {
          console.log('Broken Links Results:', response.data);
          // Handle the response as needed
        })
        .catch(error => {
          console.error('Error checking all broken links:', error);
          // Handle the error
        })
        .finally(() => {
          this.loadingCheckAll = false;
        });
    }*/
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
  width: 90%;
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

.results-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.results-table th,
.results-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

.results-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.error-message {
  color: #ff6347;
  margin-top: 10px;
}
</style>
