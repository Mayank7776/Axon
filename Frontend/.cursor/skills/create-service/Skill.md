# Skill: Create Service

This skill documents how to create entity data services in `src/app/services/` wrapping the global API helper.

## Guidelines

1. **Class Naming**: Keep class names simple as nouns matching the entity (e.g. `User`, `Blog`, `Role`) instead of suffixes like `UserService`.
2. **Inject ApiService**: Use `private api = inject(ApiService)` from `src/app/services/api`.
3. **Parameters Mapping**: Use standard HttpClient `HttpParams` to serialize filter options.
4. **Observable Return**: Ensure methods return an `Observable<any>` or strongly typed formats.

## Code Template (`src/app/services/blog.ts`)

```typescript
import { inject, Injectable } from '@angular/core';
import { HttpParams } from '@angular/common/http';
import { ApiService } from './api';
import { DataTableFilter } from '../models/datatable';

@Injectable({
  providedIn: 'root'
})
export class Blog {
  private api = inject(ApiService);

  getBlogs(filter?: DataTableFilter) {
    let params = new HttpParams();

    if (filter) {
      Object.keys(filter).forEach((key) => {
        const val = (filter as any)[key];
        if (val !== undefined && val !== null) {
          params = params.set(key, val.toString());
        }
      });
    }
    return this.api.get<any>('/blogs/list/all', params);
  }

  getBlog(id: string) {
    return this.api.get<any>(`/blogs/${id}`);
  }

  createBlog(formData: FormData) {
    return this.api.post<any>('/blogs/upsert', formData);
  }

  deleteBlog(id: string) {
    return this.api.delete<any>(`/blogs/${id}`);
  }
}
```
