import { inject, Injectable } from '@angular/core';
import { ApiService } from './api';

@Injectable({
  providedIn: 'root',
}
)
export class Auth {
  private api = inject(ApiService)

  login(payload: any) {
    return this.api.post('/auth/login', payload);
  }

  register(payload: any){
    return this.api.post('auth/register', payload);
  }

  forgotpassword(payload: any){
    return this.api.post('auth/forgout-password', payload);
  }

  resetpassword(payload: any){
    return this.api.post('auth/reset-password', payload);
  }

  validateOtp(payload:any){
    return this.api.post('auth/validate-otp', payload);
  }

  validateToken() {
    return this.api.post('/auth/validate', {});
  }

  logout() {
    return this.api.post('auth/logout', {});
  }

  clearSession() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  }
}
