import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { LoginService } from '../services/login.service';
import { Router } from '@angular/router';
import { NgForm } from '@angular/forms';
@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})

export class RegistrationComponent {
  first_name : string = '';
  last_name : string = '' ;
  email: string = '';
  username: string = '';
  password: string = '';
  confirmPassword: string = '';

  constructor(private http: HttpClient,private router: Router) {}
  ngOnInit(){
    this.email = '';
    this.username = '';
    this.password = '';
    this.confirmPassword = '';
  }
  onSubmit() {
    if (this.email === '' || this.username === '' || this.password === '' || this.confirmPassword === '') {
      window.alert('Please fill in all required fields.');
    } else if (this.password !== this.confirmPassword) {
      window.alert('Passwords do not match.');
    } else {
      this.registerUser(this.email, this.username, this.password);
    } 
  }
  
  registerUser(email : string, username : string,password :string) {
    this.http.post('http://127.0.0.1:8000/api/register/',{email,username,password}).subscribe(
        (response) => {
          console.log('Registration successful.');
          email = '';
          username = '';
          password = '';
          this.confirmPassword = '';
          this.router.navigate(['/sign-in'])
        },
        (error) => {
          console.log('Registration failed.');
          email = '';
          username = '';
          password = '';
          this.confirmPassword = '';
        }
      );
  }
}
