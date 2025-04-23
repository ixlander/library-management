import { Component } from '@angular/core';
import { LoginService } from './services/login.service';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontand';
  constructor(private loginService: LoginService) {
    const token = localStorage.getItem('token');
    if (token) {
      this.loginService.setStatus(true);
    }
  }
}
