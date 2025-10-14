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
            try {
                const token = await getAuthToken();
                if (token) {
                    config.headers.Authorization = `Bearer ${token}`;
                    console.log("Added auth token to request");
                }
            } catch (err) {
                console.error("Failed to get auth token:", err);
            }
            return config;
        },
        (error) => {
            console.error("Request interceptor error:", error);
            return Promise.reject(error);
        }
    );
};

export default api;
