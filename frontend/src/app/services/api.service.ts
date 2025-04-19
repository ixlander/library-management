import { Injectable } from '@angular/core';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private token: string | null = null;

  constructor() {}

  setToken(token: string) {
    this.token = token;
  }

  async loginUser(credentials: { username: string; password: string }) {
    const response = await axios.post(`${API_URL}/token/`, credentials);
    this.setToken(response.data.access);
    return response.data.access;
  }

  async registerUser(data: { username: string; email: string; password: string }) {
    const response = await axios.post(`${API_URL}/users/`, data);
    return response.data;
  }

  async fetchBooks() {
    const response = await axios.get(`${API_URL}/books/`);
    return response.data;
  }

  async fetchBookDetail(bookId: number) {
    const response = await axios.get(`${API_URL}/books/${bookId}/`);
    return response.data;
  }

  async addFavorite(bookId: number) {
    const response = await axios.post(`${API_URL}/books/${bookId}/add_to_favorites/`, {}, {
      headers: { Authorization: `Bearer ${this.token}` },
    });
    return response.data;
  }

  async updateReadingProgress(bookId: number, progress: number) {
    const response = await axios.post(`${API_URL}/books/${bookId}/update_progress/`, { progress }, {
      headers: { Authorization: `Bearer ${this.token}` },
    });
    return response.data;
  }

  async createReview(reviewData: { book: number; rating: number; comment: string }) {
    const response = await axios.post(`${API_URL}/reviews/`, reviewData, {
      headers: { Authorization: `Bearer ${this.token}` },
    });
    return response.data;
  }
}