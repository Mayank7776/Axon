import { inject, Injectable } from '@angular/core';
import { ApiService } from './api';

@Injectable({
  providedIn: 'root',
})
export class Role {
  private api = inject(ApiService);

  getRoles() {
    return this.api.get<any[]>('/roles');
  }

  createRole(payload: { name: string; description?: string }) {
    return this.api.post<any>('/roles', payload);
  }

  updateRole(id: string, payload: { name?: string; description?: string; is_active?: boolean }) {
    return this.api.put<any>(`/roles/${id}`, payload);
  }

  deleteRole(id: string) {
    return this.api.delete<any>(`/roles/${id}`);
  }
}
