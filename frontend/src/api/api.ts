import axios from "axios";

const axiosClient = axios.create({
    baseURL: 'http://localhost:5000', // Default base URL
  });
  
  // Interceptors (optional): To add interceptors for requests or responses
//   axiosClient.interceptors.request.use(
//     (config) => {
//       // You can modify the request config before sending the request
//       // Example: Add an authorization token dynamically
//       config.headers.Authorization = 'Bearer dynamic_token';
//       return config;
//     },
//     (error) => {
//       // Handle errors in request setup
//       return Promise.reject(error);
//     }
//   );
  
//   axiosClient.interceptors.response.use(
//     (response) => {
//       // Handle successful responses
//       return response;
//     },
//     (error) => {
//       // Handle errors in the response
//       return Promise.reject(error);
//     }
//   );
  
export default axiosClient;