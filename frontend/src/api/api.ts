import axios from "axios";

const axiosClient = axios.create({
  baseURL: "http://https://iis-vet-clinic.onrender.com", // Default base URL
  withCredentials: true, // Povolit posílání cookies přes různé domény
});

export default axiosClient;