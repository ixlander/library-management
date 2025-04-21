import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Book, Favbook } from './models';
import {map, Observable} from 'rxjs';
import { switchMap } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})

export class FavbookService {

  BASE_URL = 'http://127.0.0.1:8000/api';

  constructor(private client: HttpClient) {}

  getFavbook(book_id: number): Observable<Favbook> {
    return this.client.post<Favbook>(`${this.BASE_URL}/favbook/`,
      {
        book: book_id,
      })
  }
  addFavbook(book_id: number): Observable<Favbook> {
    return this.client.post<Favbook>(`${this.BASE_URL}/favbook-create/`,
      {
        book: book_id
      })
  }

  deleteFavbook(favbook_id: number): Observable<any> {
    return this.client.delete(`${this.BASE_URL}/favbook-delete/${favbook_id}`)
  }
}
