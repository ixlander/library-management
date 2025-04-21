import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Book, Comment } from './models';
import {map, Observable} from 'rxjs';
import { switchMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})

export class CommentService {

  BASE_URL = 'http://127.0.0.1:8000/api';

  constructor(private client: HttpClient) {}

  writeComment(book_id: number, comment: string): Observable<Comment> {
    return this.client.post<Comment>(`${this.BASE_URL}/comments-create/`, 
    {
      book: book_id,
      content: comment,
    })
  }

  updateComment(comment_id: number, book_id: number, comment: string): Observable<Comment> {
    return this.client.put<Comment>(`${this.BASE_URL}/comment-update/${comment_id}`,
    {
      book: book_id,
      content: comment 
    })
  }

  deleteComment(comment_id: number): Observable<any> {
    return this.client.delete(`${this.BASE_URL}/comment-delete/${comment_id}`)
  }
}
