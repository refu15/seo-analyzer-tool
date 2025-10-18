import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Sites API
export const sitesApi = {
  getAll: () => api.get('/api/v1/sites/'),
  getById: (siteId) => api.get(`/api/v1/sites/${siteId}`),
  create: (siteData) => api.post('/api/v1/sites/', siteData),
  delete: (siteId) => api.delete(`/api/v1/sites/${siteId}`),
};

// Analysis API
export const analysisApi = {
  runAnalysis: (siteId) => api.post(`/api/v1/analysis/${siteId}`),
  getProgress: (siteId) => api.get(`/api/v1/analysis/${siteId}/progress`),
  getLatest: (siteId) => api.get(`/api/v1/analysis/${siteId}/latest`),
  getHistory: (siteId, limit = 10) => api.get(`/api/v1/analysis/${siteId}/history?limit=${limit}`),
};

export default api;
