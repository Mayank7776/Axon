# Skill: Create Feature

This skill outlines how to build and register a new feature folder inside the Angular application.

## Feature Scaffold Pattern

1. **Create the Folder**:
   Create a dedicated subdirectory under `src/app/features/` named after your resource (e.g. `src/app/features/blogs/`).
2. **Generate files inside the folder**:
   Ensure you create these four files (omitting `.component` in naming):
   - `blogs.ts` (Component code)
   - `blogs.html` (Component view template)
   - `blogs.css` (Component style sheet)
   - `blogs.spec.ts` (Component unit tests)
3. **Register Lazy Route**:
   Add a route definition to `src/app/app.routes.ts` pointing to the component:
   ```typescript
   {
     path: 'blogs',
     loadComponent: () => import('./features/blogs/blogs').then(m => m.Blogs),
     canActivate: [authGuard]
   }
   ```

## Example Feature Component Setup (`src/app/features/blogs/blogs.ts`)

```typescript
import { Component, inject, signal, OnInit } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Blog } from '../../services/blog';

@Component({
  selector: 'app-blogs',
  imports: [],
  templateUrl: './blogs.html',
  styleUrl: './blogs.css'
})
export class Blogs implements OnInit {
  private blogService = inject(Blog);
  
  protected readonly blogs = signal<any[]>([]);
  protected readonly isLoading = signal(false);

  ngOnInit() {
    this.loadBlogs();
  }

  private loadBlogs() {
    this.isLoading.set(true);
    this.blogService.getBlogs()
      .pipe(takeUntilDestroyed())
      .subscribe({
        next: (res) => {
          this.blogs.set(res || []);
          this.isLoading.set(false);
        },
        error: () => this.isLoading.set(false)
      });
  }
}
```
