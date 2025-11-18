import axios, { AxiosError } from "axios";
import type { User } from "../interfaces";

const baseURL =
  (import.meta as any).env?.VITE_API_URL ||
  (typeof process !== "undefined" && (process as any).env?.VITE_API_URL) ||
  "http://localhost:8000";

export const api = axios.create({
  baseURL,
});

// Обробка помилок
api.interceptors.response.use(
  (res) => res,
  (err: AxiosError<any>) => {
    const status = err.response?.status;
    const data = err.response?.data as any;
    
    // rate limiting
    if (status === 429) {
      const retryAfter = (err.response as any)?.headers?.["retry-after"];
      let rateMsg = "Забагато запитів. Спробуйте ще раз трохи пізніше.";
      if (retryAfter) {
        rateMsg += ` Можна повторити запит приблизно через ${retryAfter} с.`;
      }
      return Promise.reject(new Error(rateMsg));
    }
    
    let message =
      (typeof data === "string" && data) ||
      data?.message ||
      data?.detail ||
      (Array.isArray(data?.errors) ? data.errors.map((e: any) => e.msg || e.message).join("; ") : "") ||
      err.message ||
      "Unexpected error";
    if (status) message = `[${status}] ${message}`;
    return Promise.reject(new Error(message));
  }
);

export function extractErrorMessage(error: unknown): string {
  if (error instanceof Error) return error.message;
  if (typeof error === "string") return error;
  try {
    return JSON.stringify(error);
  } catch {
    return "Unknown error";
  }
}

// Types are defined in src/interfaces/*

export async function fetchRandomUser(): Promise<User> {
  const { data } = await api.get("/external/random-user");
  return data;
}

export async function createUser(user: User): Promise<User> {
  console.log(user);
  const { data } = await api.post("/users", user);
  return data;
}

export async function listUsers(params?: { sort?: string }): Promise<User[]> {
  const { data } = await api.get("/users", { params });
  return data;
}

export async function updateUser(id: number, user: User): Promise<User> {
  const { data } = await api.put(`/users/${id}`, user);
  return data;
}

export async function deleteUser(id: number): Promise<void> {
  await api.delete(`/users/${id}`);
}


