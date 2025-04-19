import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-book-list',
  imports: [CommonModule],
  templateUrl: './book-list.component.html',
  standalone: true,
})
export class BookListComponent implements OnInit {
  books: any[] = [];

  constructor(private apiService: ApiService, private router: Router) {}

  async ngOnInit() {
    this.books = await this.apiService.fetchBooks();
  }

  viewBookDetail(bookId: number) {
    this.router.navigate([`/books/${bookId}`]);
  }
}