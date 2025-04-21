import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent {
  email : string = '';
  password : string = '';
  confirmPassword : string = '';
   
  constructor(private http : HttpClient){}
  ngOnInit(){
    this.email = '';
    this.password = '';
    this.confirmPassword = '';
  }
  updatePassword(){
    if (this.email === '' ||  this.password === '' || this.confirmPassword === '') {
      window.alert('Please fill in all required fields.');
    } else if (this.password !== this.confirmPassword) {
      window.alert('Passwords do not match.');
    } else {
      this.newPassword(this.email, this.password);
    } 
  }
  newPassword(email : string,password : string){
    this.http.post('http://127.0.0.1:8000/api/newPassword/',{email,password}).subscribe(
      (response) =>{
        this.email = '';
        this.password = '';
        this.confirmPassword = '';
        window.alert("Password was updated, try to sign-in")
      }
    )
  }
}
