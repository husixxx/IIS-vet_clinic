import axios from "axios";

const axiosClient = axios.create({
  baseURL: "http://localhost:5000", // Default base URL
  withCredentials: true, // Povolit posílání cookies přes různé domény
});

export default axiosClient;