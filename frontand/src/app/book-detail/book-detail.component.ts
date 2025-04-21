import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { BookService } from '../services/book.service';
import {Book, Comment, Review, User, Favbook, BookShelf} from '../models';
import { CommentService } from '../comment.service';
import { ReviewService } from '../review.service';
import { BookshelfService } from '../services/bookshelf.service';
import { LoginService } from '../services/login.service';
import { FavbookService } from '../favbook.service';
import {Observable, tap} from "rxjs";



@Component({
  selector: 'app-book-detail',
  templateUrl: "./book-detail.component.html",
  styleUrls: ['./book-detail.component.css']
})
export class BookDetailComponent implements OnInit {

  statusBookshelf : boolean;
  bookshelves : BookShelf[] = [];
  newBookshelf : BookShelf;
  user: User;
  book: Book;
  loaded: boolean;
  favbooks: Favbook[] =[];
  isFavbooks: boolean = false;
  link : string;
  comments: Comment[] = [];
  reviews: Review[] = [];
  extraBooks: Book[] = [];
  isExtraBooks: boolean = false;
  // For output comments and reviews
  isComments: boolean = false;
  isReviews: boolean = false;

  // For getting comment input
  comment: string = '';

  // For getting review input
  reviewComment: string = '';
  reviewRating: number = 0;
  // Update comment
  isUComment: boolean = false;
  liked: boolean = false;
  undoliked: boolean=false;

  updComment: string = '';
  likes: number;
  // Update review
  isUReview: boolean = false;
  updReviewComment: string = '';
  updRating: number = 0;

  constructor(private route: ActivatedRoute, private favbookService: FavbookService ,private bookService: BookService, private commentService: CommentService,private bookshelfService : BookshelfService, private reviewService: ReviewService, private loginService: LoginService) { // ActivatedRoute is a injectable class, that's why we don't need to create instance with 'new'
    this.book = {} as Book;
    this.newBookshelf = {} as BookShelf;
    this.statusBookshelf = false;
    this.loaded = true;
    this.link = '';
    this.likes = 0;
    this.user = {} as User;
  }

  ngOnInit(): void {

    this.bookshelfService.getBookshelves().subscribe((data:BookShelf[])=>{
      this.bookshelves = data;
    })


    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.route.paramMap.subscribe((params) => {
      const id = Number(params.get('id'));
      this.loaded = false;

      this.bookService.getBook(id).subscribe((book) => {
        this.book = book;
        this.loaded = true;
        this.link = book.link;
        this.likes = book.likes;

        this.bookService.getBooksComments(this.book.id).subscribe((data: Comment[]) => {
          this.comments = data;
          this.isComments = this.comments.length > 0;
        })



        this.bookService.getFavBooks(this.book.id).subscribe((data: Favbook[]) => {
          this.favbooks = data;
          this.isFavbooks = this.favbooks.length > 0;
        })

        this.bookService.getBooksReviews(this.book.id).subscribe((data: Review[]) => {
          this.reviews = data;
          this.isReviews = this.reviews.length > 0;
        })

        this.bookService.getBooksByPublisher(this.book.publisher).subscribe((data: Book[]) => {
          this.extraBooks = data.filter(book => book.id !== this.book.id);
          // Если this.extraBooks не пустой, то присвоить isExtraBooks = True
          this.isExtraBooks = this.extraBooks.length > 0;
        })
      })
    });

    this.loginService.getUser().subscribe(user => {
      this.user = user;
    });
  }

  addBookshelf() {
    // this.modalService.show(BookshelfCreateComponent,);
    this.statusBookshelf = true;
  }
  addBook(){

  }
  createBookshelf(){

  }
  submitReview() {
    this.reviewService.createReview(this.book.id, this.reviewComment, this.reviewRating).subscribe((data: Review) => {
      this.reviews.push(data);
      this.reviewComment = '';
    })
  }

  submitCommet() {
    this.commentService.writeComment(this.book.id, this.comment).subscribe((data: Comment) => {
      this.comments.push(data);
      this.comment = '';
    })
  }
  telega(){
    window.open(`https://t.me/share/url?url=${this.link}&text=xssxcfscxscsc`)
  }



  deleteComment(comment_id: number) {
    this.commentService.deleteComment(comment_id).subscribe((data: any) => {
      this.comments = this.comments.filter((comment) => comment.id !== comment_id)
    })
  }

  deleteReview(review_id: number) {
    this.reviewService.deleteReview(review_id).subscribe((data: any) => {
      this.reviews = this.reviews.filter((review) => review.id !== review_id)
    })
  }

  updateComment(comment_id: number) {
    this.commentService.updateComment(comment_id, this.book.id, this.updComment).subscribe((data: Comment) => {
      this.updComment = '';
      const index = this.comments.findIndex(comment => comment.id === data.id);
      if (index !== -1) {
        this.comments[index] = data;
      }
    })
  }

  updateReview(review_id: number) {
    this.reviewService.updateReview(review_id, this.book.id, this.updReviewComment, this.updRating).subscribe((data: any) => {
      this.updReviewComment = '';
      const index = this.reviews.findIndex(review => review.id === data.id);
      if (index !== -1) {
        this.reviews[index] = data;
      }
    })
  }

  setComment() {
    this.isUComment = !this.isUComment;
  }

  setReview() {
    this.isUReview = !this.isUReview;
    console.log(this.isUComment);
  }


  submitFavbook() {
    this.favbookService.addFavbook(this.book.id).subscribe((data: Favbook) => {
      this.favbooks.push(data);
    })
  }

  likeBook() {
    if (!this.liked) {
      this.bookService.booklike(this.book.id).subscribe((data: Book) => {
        this.likes = data.likes;
        this.liked = true;
        this.undoliked=false;
      });
    }
  }

  undolikeBook() {
    if (!this.undoliked) {
      this.bookService.undobooklike(this.book.id).subscribe((data: Book) => {
        this.likes = data.likes;
        this.undoliked = true;
        this.liked = false;
      });
    }
  }



}
