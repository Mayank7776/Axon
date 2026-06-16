import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = environment.apiUrl;
  private http = inject(HttpClient);

  private getFullUrl(endpoint: string): string {
    const cleanBase = this.baseUrl.endsWith('/') ? this.baseUrl.slice(0, -1) : this.baseUrl;
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${cleanBase}${cleanEndpoint}`;
  }

  get<T>(endpoint: string, params?: HttpParams ): Observable<T> {
    return this.http.get<T>(
      this.getFullUrl(endpoint),
      { params }
    );
  }

  post<T>(endpoint: string, body: any ): Observable<T> {
    return this.http.post<T>(
      this.getFullUrl(endpoint),
      body
    );
  }

  put<T>(endpoint: string, body: any ): Observable<T> {
    return this.http.put<T>(
      this.getFullUrl(endpoint),
      body
    );
  }

  patch<T>( endpoint: string, body: any ): Observable<T> {
    return this.http.patch<T>(
      this.getFullUrl(endpoint),
      body
    );
  }

  delete<T>( endpoint: string ): Observable<T> {
    return this.http.delete<T>(
      this.getFullUrl(endpoint)
    );
  }
}