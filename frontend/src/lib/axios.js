import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000", // Your backend URL
    headers: {
        "Content-Type": "application/json",
    },
});

export const setupAxiosInterceptors = (getAuthToken) => {
    api.interceptors.request.use(
        async (config) => {
            const token = await getAuthToken();
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
            return config;
        },
        (error) => {
            return Promise.reject(error);
        }
    );
};

export default api;
