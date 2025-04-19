import { Component } from '@angular/core';
import { ApiService } from '../services/api.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register',
  imports: [FormsModule],
  templateUrl: './register.component.html',
  standalone: true,
})
export class RegisterComponent {
  username: string = '';
  email: string = '';
  password: string = '';

  constructor(private apiService: ApiService) {}

  async register() {
    try {
      await this.apiService.registerUser({
        username: this.username,
        email: this.email,
        password: this.password,
      });
      alert('Registration successful!');
    } catch (error) {
      alert('Registration failed!');
    }
  }
}