// src/api/axiosInstance.js
import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 200000,
  headers: {
    'Content-Type': 'application/json',
    // podés agregar Authorization aquí si es necesario, en este caso no
  },
});

export default axiosInstance;
