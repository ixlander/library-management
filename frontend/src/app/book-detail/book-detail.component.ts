import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../services/api.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-book-detail',
  imports: [FormsModule],
  templateUrl: './book-detail.component.html',
  standalone: true,
})
export class BookDetailComponent {
  book: any = {};
  progress: number = 0;
  review = { rating: 0, comment: '' };

  constructor(private route: ActivatedRoute, private apiService: ApiService) {}

  async ngOnInit() {
    const bookId = +this.route.snapshot.paramMap.get('id')!;
    this.book = await this.apiService.fetchBookDetail(bookId);
  }

  async addToFavorites() {
    await this.apiService.addFavorite(this.book.book_id);
    alert('Book added to favorites!');
  }

  async updateProgress() {
    await this.apiService.updateReadingProgress(this.book.book_id, this.progress);
    alert('Reading progress updated!');
  }

  async submitReview() {
    await this.apiService.createReview({ book: this.book.book_id, ...this.review });
    alert('Review submitted!');
  }
}