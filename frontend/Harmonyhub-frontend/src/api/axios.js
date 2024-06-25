import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000/api/',  // your Django API URL
});

export default axiosInstance;
