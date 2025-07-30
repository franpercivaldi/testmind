import axiosInstance from './axiosInstance';

// Funcion para listar los archivos excel
const listFiles = async () => {
  const response = await axiosInstance.get('/excel/list');
  return response.data;
};

// Funcion para siubir excel
const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axiosInstance.post('/excel/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};


// Funcion para traer los tickets de jira de X proyecto
const getJiraIssues = async ({ projectKey, issueType = null, status = 'QA TESTING', maxResults = 20}) => {
  const params = {
    status: status,
    project_key: projectKey,
    max_results: maxResults
  };

  if (issueType) params.issue_type = issueType;

  const response = await axiosInstance.get('/jira/issues', { params });
  return response.data;
};

// Funcion para crear los casos de prueba
export const generateTestCases = async (data) => {
  const response = await axiosInstance.post('/test-cases/generate', data);
  return response.data;
};


export { uploadFile, listFiles, getJiraIssues };