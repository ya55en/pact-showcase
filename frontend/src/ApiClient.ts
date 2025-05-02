import axios, { AxiosInstance, AxiosResponse } from 'axios';

export class ApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = axios.create({
      baseURL,
      timeout: 5000,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  async get<T>(url: string): Promise<T> {
    const res = await this.client.get<T>(url);
    this.handleError(res);
    return res.data;
  }

  async post<T>(url: string, data: unknown): Promise<T> {
    const res = await this.client.post<T>(url, data);
    this.handleError(res);
    return res.data;
  }

  private handleError(res: AxiosResponse) {
    if (res.status < 200 || res.status >= 300) {
      throw new Error(`HTTP error ${res.status}: ${res.statusText}`);
    }
  }
}
