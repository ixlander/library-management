import { Component, OnInit } from '@angular/core';
import { SignInComponent } from '../sign-in/sign-in.component';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-top-panel',
  templateUrl: './top-panel.component.html',
  styleUrls: ['./top-panel.component.css']
})
export class TopPanelComponent implements OnInit{
  logged : boolean = false;
  constructor(private loginService : LoginService){}
  ngOnInit(): void {
    this.loginService.logged.subscribe(value=> this.logged = value)
    const token = localStorage.getItem('token');
    if(token){
    this.logged = true;
    }
  }
  logout(){
    localStorage.removeItem("token");
    this.logged = false;
    this.updateStatus()
    
  }
  updateStatus(){
    this.loginService.setStatus(false);
  }
}
