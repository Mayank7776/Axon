import { inject, Injectable } from '@angular/core';
import { HttpParams } from '@angular/common/http';
import { ApiService } from './api';

@Injectable({
  providedIn: 'root',
})
export class Myworkout {
  private api = inject(ApiService);

  getAllPlans(userId: string) {
    const params = new HttpParams().set('user_id', userId);
    return this.api.get<any[]>('/workout/all-plan', params);
  }

  getPlan(id: string) {
    return this.api.get<any>(`/workout/plan/${id}`);
  }

  upsertPlan(payload: any) {
    return this.api.post<any>('/workout/upsert-plan', payload);
  }

  deletePlan(id: string) {
    return this.api.delete<any>(`/workout/delete-plan/${id}`);
  }

  getAllDays(planId: string) {
    const params = new HttpParams().set('plan_id', planId);
    return this.api.get<any[]>('/workout/all-day', params);
  }

  getDay(id: string) {
    return this.api.get<any>(`/workout/day/${id}`);
  }

  upsertDay(payload: any) {
    return this.api.post<any>('/workout/upsert-day', payload);
  }

  deleteDay(id: string) {
    return this.api.delete<any>(`/workout/delete-day/${id}`);
  }

  saveAIPlan(payload: any) {
    return this.api.post<any>('/workout/save-ai-plan', payload);
  }

  getActiveDay(userId: string, date?: string) {
    let params = new HttpParams().set('user_id', userId);
    if (date) {
      params = params.set('date', date);
    }
    return this.api.get<any>('/workout/active-day', params);
  }

  saveWorkoutStats(payload: any) {
    return this.api.post<any>('/workout/save-workout-stats', payload);
  }

  getWorkoutStats(userId: string) {
    return this.api.get<any>(`/workout/workout-stats/${userId}`);
  }
}
