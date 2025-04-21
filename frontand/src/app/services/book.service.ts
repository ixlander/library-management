import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { Observable } from 'rxjs';
import { AuthToken, } from '../models';

import { Book, Category, Review, Comment, Favbook } from '../models';


@Injectable({
  providedIn: 'root'
})

export class BookService {
  BASE_URL = 'http://127.0.0.1:8000/api';
  logged: boolean = false;

  constructor(private client: HttpClient) {}

  getCategories(): Observable<Category[]> {
    return this.client.get<Category[]>(`${this.BASE_URL}/categories/`)
  }

  getBooks(): Observable<Book[]> {
    return this.client.get<Book[]>(`${this.BASE_URL}/books/`)
  }

  getCategoryBooks(category_id: number): Observable<Book[]> {
    return this.client.get<Book[]>(`${this.BASE_URL}/categories/${category_id}/books`)
  }

  getBook(book_id: number): Observable<Book> {
    return this.client.get<Book>(`${this.BASE_URL}/books/${book_id}`)
  }

  getBooksReviews(id: number): Observable<Review[]> {
    return this.client.get<Review[]>(`${this.BASE_URL}/books/${id}/reviews/`)
  }

  getBooksComments(id: number): Observable<Comment[]> {
    console.log(id)
    return this.client.get<Comment[]>(`${this.BASE_URL}/books/${id}/comments/`)
  }

  getBooksByPublisher(publisher: string): Observable<Book[]> {
    return this.client.get<Book[]>(`${this.BASE_URL}/books-by-publisher/${publisher}/`)
  }

  getFavBooks(id: number): Observable<Favbook[]> {
    return this.client.get<Favbook[]>(`${this.BASE_URL}/favbook/`)
  }

  booklike(id:number):Observable<Book>{
    return this.client.get<Book>(`${this.BASE_URL}/book/${id}/like`)
  }

  undobooklike(id:number):Observable<Book>{
    return this.client.get<Book>(`${this.BASE_URL}/book/${id}/undolike`)
  }


}
