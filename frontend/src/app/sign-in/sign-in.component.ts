import { Component, OnInit } from '@angular/core';
import { AuthToken } from '../models';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})
export class SignInComponent implements OnInit {
  logged: boolean | undefined;
  username: string = '';
  password: string = '';

  constructor(private loginService: LoginService) {}

  ngOnInit() {
    this.loginService.logged.subscribe(value => this.logged = value);
    const token = localStorage.getItem('token');
    if (token) {
      this.loginService.setStatus(true);
    }
  }

  login() {
    this.loginService.login(this.username, this.password).subscribe((data: AuthToken) => {
      console.log('LOGIN RESPONSE:', data);
      localStorage.setItem('token', data.access); 
      this.loginService.setStatus(true);
    }, error => {
      console.error('Login failed:', error);
    });
  }
}
