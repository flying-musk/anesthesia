import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Handle unauthorized
      console.error('Unauthorized access');
    }
    return Promise.reject(error);
  }
);

// Patient API
export const patientAPI = {
  // Get all patients
  getPatients: (params = {}) => api.get('/patients', { params }),
  
  // Get patient by ID
  getPatient: (id) => api.get(`/patients/${id}`),
  
  // Create patient
  createPatient: (data) => api.post('/patients', data),
  
  // Update patient
  updatePatient: (id, data) => api.put(`/patients/${id}`, data),
  
  // Delete patient
  deletePatient: (id) => api.delete(`/patients/${id}`),
  
  // Search patient
  searchPatient: (data) => api.post('/patients/search', data),
  
  // Get patient medical history
  getMedicalHistory: (id) => api.get(`/patients/${id}/medical-history`),
  
  // Create patient medical history
  createMedicalHistory: (id, data) => api.post(`/patients/${id}/medical-history`, data),
  
  // Update patient medical history
  updateMedicalHistory: (id, data) => api.put(`/patients/${id}/medical-history`, data),
  
  // Get patient surgery records
  getSurgeryRecords: (id) => api.get(`/patients/${id}/surgery-records`),
  
  // Create patient surgery record
  createSurgeryRecord: (id, data) => api.post(`/patients/${id}/surgery-records`, data),
};

// Anesthesia Guidelines API
export const anesthesiaAPI = {
  // Generate guideline
  generateGuideline: (data) => api.post('/anesthesia/guidelines/generate', data),
  
  // Get all guidelines
  getGuidelines: (params = {}) => api.get('/anesthesia/guidelines', { params }),
  
  // Get guideline by ID
  getGuideline: (id) => api.get(`/anesthesia/guidelines/${id}`),
  
  // Update guideline
  updateGuideline: (id, data) => api.put(`/anesthesia/guidelines/${id}`, data),
  
  // Delete guideline
  deleteGuideline: (id) => api.delete(`/anesthesia/guidelines/${id}`),
  
  // Get patient guidelines
  getPatientGuidelines: (patientId) => api.get(`/anesthesia/guidelines/patient/${patientId}`),
  
  // Get guidelines by date
  getGuidelinesByDate: (date) => api.get(`/anesthesia/guidelines/by-date?surgery_date=${date}`),
  
  // Template API
  getTemplates: (params = {}) => api.get('/anesthesia/templates', { params }),
  getTemplate: (id) => api.get(`/anesthesia/templates/${id}`),
  createTemplate: (data) => api.post('/anesthesia/templates', data),
  updateTemplate: (id, data) => api.put(`/anesthesia/templates/${id}`, data),
  deleteTemplate: (id) => api.delete(`/anesthesia/templates/${id}`),
  getTemplatesByType: (type) => api.get(`/anesthesia/templates/by-type?anesthesia_type=${type}`),
};

// Health check API
export const healthAPI = {
  check: () => api.get('/health'),
};

export default api;
