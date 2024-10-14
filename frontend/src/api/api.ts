import axios from "axios";

const axiosClient = axios.create({
  baseURL: "http://localhost:5000", // Default base URL
  withCredentials: true, // Povolit posílání cookies přes různé domény
});

// Interceptors (optional): To add interceptors for requests or responses
axiosClient.interceptors.request.use(
  (config) => {
    // Můžeme ponechat request interceptor prázdný, protože nebudeme přidávat Authorization hlavičku
    return config;
  },
  (error) => {
    // Handle errors in request setup
    return Promise.reject(error);
  }
);

axiosClient.interceptors.response.use(
  (response) => {
    // Handle successful responses
    return response;
  },
  (error) => {
    // Handle errors in the response
    return Promise.reject(error);
  }
);

export default axiosClient;