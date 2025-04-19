import { Component } from '@angular/core';
import { ApiService } from '../services/api.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  imports: [FormsModule],
  templateUrl: './login.component.html',
  standalone: true
})
export class LoginComponent {
  username: string = '';
  password: string = '';

  constructor(private apiService: ApiService) {}

  async login() {
    try {
      await this.apiService.loginUser({ username: this.username, password: this.password });
      alert('Login successful!');
    } catch (error) {
      alert('Login failed!');
    }
  }
}