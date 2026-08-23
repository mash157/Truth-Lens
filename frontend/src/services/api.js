import { API_BASE_URL } from '../utils/constants';

/**
 * Helper to handle fetch responses and raise errors on HTTP issues.
 */
async function apiRequest(path, options = {}) {
  const url = `${API_BASE_URL}${path}`;
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };
  
  const response = await fetch(url, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  });
  
  if (!response.ok) {
    let errorDetail = 'API Request Failed';
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.detail || errorDetail;
    } catch (_) {}
    
    // Package it as a clean object
    const err = new Error(typeof errorDetail === 'object' ? JSON.stringify(errorDetail) : errorDetail);
    err.status = response.status;
    err.detail = errorDetail;
    throw err;
  }
  
  return response.json();
}

export const api = {
  getHealth: () => apiRequest('/api/health'),
  
  analyzeNews: (title, text) => 
    apiRequest('/api/analyze', {
      method: 'POST',
      body: JSON.stringify({ title, text }),
    }),
    
  getMetrics: () => apiRequest('/api/metrics'),
  
  getModelInfo: () => apiRequest('/api/model-info'),
  
  getFeatureImportance: () => apiRequest('/api/feature-importance'),
  
  getSampleArticles: () => apiRequest('/api/sample-articles'),
  
  getConfusionMatrixUrl: () => `${API_BASE_URL}/api/metrics/confusion-matrix`,
};
