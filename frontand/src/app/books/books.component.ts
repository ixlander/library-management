import { Component, OnInit } from '@angular/core';
import { Book, Category } from '../models';
import { BookService } from '../services/book.service';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-books',
  templateUrl: './books.component.html',
  styleUrls: ['./books.component.css']
})
export class BooksComponent implements OnInit {
  logged : boolean | undefined;
  books: Book[] = [];
  categories: Category[] = [];
  categoryBooks: Book[] = [];
  currentCategory: string = 'All';
  currentSorting: string = 'None';

  searchText: string = '';

  constructor(private bookService: BookService, private loginService : LoginService) {}

  ngOnInit(): void {
    this.bookService.getBooks().subscribe((data: Book[]) => {
      this.books = data;
    })
    this.loginService.logged.subscribe(value=> this.logged = value)

    this.bookService.getCategories().subscribe((data: Category[]) => {
      this.categories = data;
    })
  }

  getCategoryBooks(category: Category) {
    if(this.currentCategory == 'All') {
      this.bookService.getCategoryBooks(category.id).subscribe((data: Book[]) => {
        this.books = data;
        this.currentCategory = category.name;
      })
    } else {
      this.bookService.getBooks().subscribe((data: Book[]) => {
        this.books = data;
        this.currentCategory = 'All';
      })
    }
  }

  sortByYear() {
    this.books.sort(  );
  }

  sortByRating() {

  }
}
