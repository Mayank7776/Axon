import { inject, Injectable } from '@angular/core';
import { HttpParams } from '@angular/common/http';
import { ApiService } from './api';

@Injectable({
  providedIn: 'root',
})
export class Chat {
  private api = inject(ApiService);

  getSessions(userId: string) {
    const params = new HttpParams().set('user_id', userId);
    return this.api.get<any[]>('/chat/sessions', params);
  }

  getSession(sessionId: string) {
    return this.api.get<any>(`/chat/sessions/${sessionId}`);
  }

  createSession(payload: { user_id: string; title: string }) {
    return this.api.post<any>('/chat/sessions', payload);
  }

  updateSession(sessionId: string, payload: { title: string }) {
    return this.api.patch<any>(`/chat/sessions/${sessionId}`, payload);
  }

  deleteSession(sessionId: string) {
    return this.api.delete<any>(`/chat/sessions/${sessionId}`);
  }

  getMessages(sessionId: string) {
    return this.api.get<any[]>(`/chat/sessions/${sessionId}/messages`);
  }

  sendMessage(payload: { session_id: string; message_content: string; role: string }) {
    return this.api.post<any>('/chat/messages', payload);
  }
}
