import { inject, Injectable } from '@angular/core';
import { HttpParams } from '@angular/common/http';
import { ApiService } from './api';

@Injectable({
  providedIn: 'root',
})
export class Notification {
  private api = inject(ApiService);

  getNotifications(userId: string) {
    const params = new HttpParams().set('user_id', userId);
    return this.api.get<any[]>('/notifications', params);
  }

  addNotification(payload: { title: string; message: string; type?: string; redirect_url?: string }) {
    return this.api.post<any>('/notifications', payload);
  }

  markRead(id: string, userId: string) {
    return this.api.patch<any>(`/notifications/${id}/read`, { user_id: userId });
  }

  markAllRead(userId: string) {
    return this.api.patch<any>('/notifications/read-all', { user_id: userId });
  }

  deleteNotification(id: string) {
    return this.api.delete<any>(`/notifications/${id}`);
  }
}
