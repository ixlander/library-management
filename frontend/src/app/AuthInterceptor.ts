import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpEvent, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = localStorage.getItem('token');
    
    console.log('Interceptor running. Token exists:', !!token);
    
    if(token) {
        const newReq = req.clone({
            headers: req.headers.set('Authorization', `Bearer ${token}`),  
        });
        return next.handle(newReq);
    }
    return next.handle(req);
  
  }

}
