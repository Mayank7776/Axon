import { inject, Injectable } from '@angular/core';
import { ApiService } from './api';

@Injectable({
  providedIn: 'root',
})
export class Blog {
  private api = inject(ApiService);

  getCategories() {
    return this.api.get<any[]>('/blogs/categories');
  }

  listBlogs(category: string) {
    return this.api.get<any[]>(`/blogs/list/${category}`);
  }

  upsertBlog(formData: FormData) {
    return this.api.post<any>('/blogs/upsert', formData);
  }

  deleteBlog(id: string) {
    return this.api.delete<any>(`/blogs/${id}`);
  }
}
