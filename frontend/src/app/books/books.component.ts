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
    console.log("Token exists:", !!localStorage.getItem('token'));
    
    this.bookService.getBooks().subscribe(
      (data: Book[]) => {
        this.books = data;
        console.log('Books loaded successfully', data.length);
      },
      error => {
        console.error('Error loading books:', error);
      }
    );
    
    this.loginService.logged.subscribe(value => this.logged = value);

    this.bookService.getCategories().subscribe(
      (data: Category[]) => {
        this.categories = data;
        console.log('Categories loaded successfully', data.length);
      },
      error => {
        console.error('Error loading categories:', error);
      }
    );
  }

  getCategoryBooks(category: Category) {
    if(this.currentCategory === 'All') {
      this.bookService.getCategoryBooks(category.id).subscribe(
        (data: Book[]) => {
          this.books = data;
          this.currentCategory = category.name;
        },
        error => {
          console.error(`Error loading books for category ${category.id}:`, error);
        }
      );
    } else {
      this.bookService.getBooks().subscribe(
        (data: Book[]) => {
          this.books = data;
          this.currentCategory = 'All';
        },
        error => {
          console.error('Error loading all books:', error);
        }
      );
    }
  }

  sortByYear() {
    this.books.sort((a, b) => {
      return (a.year || 0) - (b.year || 0);
    });
  }

  sortByRating() {
    this.books.sort((a, b) => {
      return (b.rating || 0) - (a.rating || 0);
    });
  }
}