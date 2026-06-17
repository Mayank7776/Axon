import { inject, Injectable } from '@angular/core';
import { HttpParams } from '@angular/common/http';
import { ApiService } from './api';
import { DataTableFilter } from '../models/datatable';

@Injectable({
  providedIn: 'root',
})
export class User {
  private api = inject(ApiService);

  getUsers(filter?: DataTableFilter) {
    let params = new HttpParams();

    if (filter) {
      Object.keys(filter).forEach((key) => {
        const val = (filter as any)[key];

        if (val !== undefined && val !== null) {
          params = params.set(key, val.toString());
        }
      });
    }
    
    return this.api.get<any>('/users', params);
  }

  getUser(id: string) {
    return this.api.get<any>(`/users/${id}`);
  }

  createUser(formData: FormData) {
    return this.api.post<any>('/users', formData);
  }

  updateUser(id: string, formData: FormData) {
    return this.api.put<any>(`/users/${id}`, formData);
  }

  deleteUser(id: string) {
    return this.api.delete<any>(`/users/${id}`);
  }
}
