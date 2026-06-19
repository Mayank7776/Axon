# Skill: Create Form

This skill details how to build and validate strongly-typed forms using Angular's Reactive Forms API.

## Guidelines

1. **Imports**: Import `ReactiveFormsModule`, `FormGroup`, `FormControl`, `Validators` in the component decorator configuration.
2. **Form Construction**:
   Use class-level variables with explicit controls definition:
   ```typescript
   import { FormGroup, FormControl, Validators } from '@angular/forms';

   protected readonly profileForm = new FormGroup({
     username: new FormControl('', {
       nonNullable: true,
       validators: [Validators.required, Validators.minLength(3)]
     }),
     email: new FormControl('', {
       nonNullable: true,
       validators: [Validators.required, Validators.email]
     })
   });
   ```
3. **Validation States**:
   Implement inline visual checkers to display form errors only when fields are dirty/touched:
   ```typescript
   get emailControl() {
     return this.profileForm.controls.email;
   }
   ```
4. **Submissions**:
   Disable submit buttons while the form is invalid:
   ```html
   <button [disabled]="profileForm.invalid">Submit</button>
   ```

## Example Integration

### Component file (`src/app/features/profile/profile.ts`)
```typescript
import { Component, inject } from '@angular/core';
import { FormGroup, FormControl, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-profile',
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './profile.html',
  styleUrl: './profile.css'
})
export class Profile {
  protected readonly form = new FormGroup({
    email: new FormControl('', {
      nonNullable: true,
      validators: [Validators.required, Validators.email]
    })
  });

  onSubmit() {
    if (this.form.invalid) return;
    console.log(this.form.getRawValue());
  }
}
```

### Template HTML (`src/app/features/profile/profile.html`)
```html
<form [formGroup]="form" (ngSubmit)="onSubmit()" class="flex flex-col gap-4 max-w-md mx-auto p-6 bg-slate-900 text-white rounded-lg shadow">
  <div class="flex flex-col gap-1">
    <label for="email" class="text-sm font-semibold">Email Address</label>
    <input id="email" formControlName="email" type="email" 
           class="p-2 border rounded bg-slate-800 border-slate-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500" />
    <span *ngIf="form.controls.email.touched && form.controls.email.invalid" class="text-xs text-red-500">
      Please enter a valid email.
    </span>
  </div>
  <button type="submit" [disabled]="form.invalid" class="p-2 bg-blue-600 hover:bg-blue-700 rounded transition font-semibold disabled:opacity-50">
    Update Profile
  </button>
</form>
```
