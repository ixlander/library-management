import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Review } from './models';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ReviewService {

  BASE_URL = 'http://127.0.0.1:8000/api';

  constructor(private client: HttpClient) { }

  // submitReview() {
  //   this.reviewService.createReview(this.reviewComment, this.reviewRating).subscribe((data: Review) => {
  //     this.reviews.push(data);
  //     this.reviewComment = '';
  //   })
  // }

  createReview(book_id: number, reviewComment: string, reviewRating: number): Observable<Review> {
    console.log(reviewRating) 
    console.log(book_id)
    console.log(reviewComment)
    return this.client.post<Review>(`${this.BASE_URL}/review-create/`,
    {
      book: book_id,
      rating: reviewRating,
      comment: reviewComment
    })
  }

  deleteReview(review_id: number): Observable<any> {
    return this.client.delete<any>(`${this.BASE_URL}/review-delete/${review_id}`)
  }

  updateReview(review_id: number, book_id: number, newComment: string, newRating: number): Observable<Review> {
    return this.client.put<Review>(`${this.BASE_URL}/review-update/${review_id}`, 
    {
      book: book_id,
      rating: newRating,
      comment: newComment
    })
  }
}
