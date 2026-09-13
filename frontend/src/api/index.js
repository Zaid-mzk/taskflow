import api from "./client";

export const authApi = {
  signup: (payload) => api.post("/auth/signup", payload).then((r) => r.data),
  login: (payload) => api.post("/auth/login", payload).then((r) => r.data),
};

export const projectsApi = {
  list: () => api.get("/projects").then((r) => r.data),
  create: (payload) => api.post("/projects", payload).then((r) => r.data),
  get: (id) => api.get(`/projects/${id}`).then((r) => r.data),
  remove: (id) => api.delete(`/projects/${id}`).then((r) => r.data),
};

export const tasksApi = {
  list: (projectId, status) =>
    api
      .get(`/projects/${projectId}/tasks`, { params: status ? { status } : {} })
      .then((r) => r.data),
  create: (projectId, payload) =>
    api.post(`/projects/${projectId}/tasks`, payload).then((r) => r.data),
  update: (taskId, payload) => api.patch(`/tasks/${taskId}`, payload).then((r) => r.data),
  remove: (taskId) => api.delete(`/tasks/${taskId}`).then((r) => r.data),
};
