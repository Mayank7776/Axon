# Skill: Create API Integration

This skill documents how to subscribe to backend service layers and bind records to components.

## Guidelines

1. **State Injection**:
   Use signals to bind remote resource items and network statuses:
   ```typescript
   protected readonly records = signal<any[]>([]);
   protected readonly isSearching = signal<boolean>(false);
   ```
2. **Subscription Management**:
   Never forget to bind unsubscription listeners (`takeUntilDestroyed()`) to prevent resource leaks when components destroy.
3. **Action Pipelines**:
   Structure state updates inside subscription blocks:
   - Call `.set(true)` on loading signals before invoking HTTP triggers.
   - Run updates to local arrays inside `next()`.
   - Ensure loading states are reset to `false` inside both `next` and `error` blocks or inside a `finalize` cleanup block.

## Example Request Wiring

```typescript
import { Component, inject, signal, OnInit } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { finalize } from 'rxjs';
import { User } from '../../services/user';

@Component({
  selector: 'app-users-view',
  templateUrl: './users-view.html'
})
export class UsersView implements OnInit {
  private userService = inject(User);

  protected readonly usersList = signal<any[]>([]);
  protected readonly isProcessing = signal<boolean>(false);

  ngOnInit() {
    this.fetchUsers();
  }

  fetchUsers() {
    this.isProcessing.set(true);

    this.userService.getUsers()
      .pipe(
        finalize(() => this.isProcessing.set(false)),
        takeUntilDestroyed()
      )
      .subscribe({
        next: (response) => {
          if (response?.success && response?.data) {
            this.usersList.set(response.data.items || []);
          }
        },
        error: (err) => {
          console.error('Failed to retrieve user items:', err);
        }
      });
  }
}
```
