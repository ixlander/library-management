import {Component, OnInit} from '@angular/core';
import {LoginService} from "../services/login.service";
import {Router} from "@angular/router";
import {AuthToken} from "../models";


@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit{
  logged: boolean = false;
  username: string = '';
  password: string = '';
  constructor(private router: Router,
              private loginService: LoginService,
  ) {
  }

  ngOnInit(){
    this.loginService.logged.subscribe(value=> this.logged = value)
    const token = localStorage.getItem('token');
    if(token){
      this.logged = true;
      this.updateStatus();
    }
  }
  login(){
    this.loginService.login(this.username, this.password).subscribe((data) =>{
      localStorage.setItem('token',data.token);
      this.logged = true;
      this.username = '';
      this.password = '';
      this.updateStatus();
    })
  }
  updateStatus(){
    this.loginService.setStatus(true)
  }
  logout(){
    localStorage.removeItem('token');
    this.logged = false;
  }

}
