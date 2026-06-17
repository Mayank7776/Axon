import { inject, Injectable } from '@angular/core';
import { HttpParams } from '@angular/common/http';
import { ApiService } from './api';

@Injectable({
  providedIn: 'root',
})
export class Muscles {
  private api = inject(ApiService);

  getMuscleGroups() {
    return this.api.get<any[]>('/musclegroup/get-musclegroup');
  }

  getMuscleGroup(id: string) {
    return this.api.get<any>(`/musclegroup/get-musclegroup/${id}`);
  }

  upsertMuscleGroup(formData: FormData) {
    return this.api.post<any>('/musclegroup/upsert-musclegroup', formData);
  }

  deleteMuscleGroup(id: string) {
    return this.api.post<any>(`/musclegroup/delete-musclegroup/${id}`, {});
  }

  getExercises(muscleGroupId: string) {
    const params = new HttpParams().set('id', muscleGroupId);
    return this.api.get<any[]>('/musclegroup/get-all-excercise', params);
  }

  getExercise(id: string) {
    return this.api.get<any>(`/musclegroup/get-excercise/${id}`);
  }

  upsertExercise(formData: FormData) {
    return this.api.post<any>('/musclegroup/upsert-excercise', formData);
  }

  deleteExercise(id: string) {
    return this.api.post<any>(`/musclegroup/delete-excercise/${id}`, {});
  }
}
