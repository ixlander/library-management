import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BookShelf } from '../models';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class BookshelfService {
  BASE_URL = 'http://127.0.0.1:8000/api';
  constructor(private client : HttpClient) { }
  getBookshelves(): Observable<BookShelf[]>{
    return this.client.get<BookShelf[]>(`${this.BASE_URL}/bookshelves/`)
  }
}
