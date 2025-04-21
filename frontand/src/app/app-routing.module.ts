import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { BooksComponent } from './books/books.component';
import { SignInComponent } from './sign-in/sign-in.component';
import { NotFoundComponent } from './not-found/not-found.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { BookDetailComponent } from './book-detail/book-detail.component';
import { RegistrationComponent } from './registration/registration.component';
import { PersonalPageComponent } from './personal-page/personal-page.component';
import { AboutComponent } from './about/about.component';


const routes: Routes = [

  { path: 'home', component: HomeComponent },
  { path: 'registration', component: RegistrationComponent },
  { path: 'books', component: BooksComponent },
  { path: 'books/:id', component: BookDetailComponent },
  { path: 'personal-page', component: PersonalPageComponent },
  { path: 'sign-in', component: SignInComponent },
  { path: 'sign-up', component: RegistrationComponent },
  { path: 'password', component: ForgotPasswordComponent },
  { path: 'about', component: AboutComponent},
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: '**', component: NotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
