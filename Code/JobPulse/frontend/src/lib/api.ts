import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const setAuthToken = (token: string | null) => {
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common["Authorization"];
  }
};

export const authApi = {
  getMe: () => api.get("/api/v1/auth/me"),
};

export const scrapingApi = {
  startScrape: (data: { job_title: string; location?: string; sources: string[]; date_posted?: string }) =>
    api.post("/api/v1/scraping/start", data),
  getTaskStatus: (taskId: string) => api.get(`/api/v1/scraping/tasks/${taskId}`),
  getJobs: () => api.get("/api/v1/scraping/jobs"),
  getHistory: () => api.get("/api/v1/scraping/history"),
};

export const creditsApi = {
  getBalance: () => api.get("/api/v1/credits/balance"),
  createTopup: (data: { pack_type: string; razorpay_payment_id: string }) =>
    api.post("/api/v1/credits/topup", data),
  getTransactions: () => api.get("/api/v1/credits/transactions"),
};

export const subscriptionsApi = {
  getStatus: () => api.get("/api/v1/subscriptions/status"),
  create: (plan_type: string) => api.post("/api/v1/subscriptions/create", { plan_type }),
};

export const exportsApi = {
  generate: (file_format: string = "xlsx") => api.post("/api/v1/exports/generate", null, { params: { file_format } }),
  download: (filename: string) => `${API_URL}/api/v1/exports/download/${filename}`,
  getHistory: () => api.get("/api/v1/exports/history"),
};
