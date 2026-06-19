# Skill: Create Component

This skill details the configuration of standalone Angular components.

## Guidelines

1. **Omit `.component`**: Ensure filenames are simple basenames (e.g. `workout-card.ts`, `workout-card.html`).
2. **Metadata properties**:
   - `selector`: prefixed with `app-` (e.g. `'app-workout-card'`).
   - `imports`: declare layout components, RouterOutlet, forms elements, and direct widgets required by the template.
   - `templateUrl`: relative link (e.g. `'./workout-card.html'`).
   - `styleUrl`: relative link (e.g. `'./workout-card.css'`).
3. **Signal State**: Keep variables inside the component class using Angular Signals:
   - `myVar = signal(initialValue)`
   - Read signals using parenthesis in code or template: `myVar()`

## Code Template (`src/app/shared/workout-card/workout-card.ts`)

```typescript
import { Component, input, output } from '@angular/core';

@Component({
  selector: 'app-workout-card',
  imports: [],
  templateUrl: './workout-card.html',
  styleUrl: './workout-card.css'
})
export class WorkoutCard {
  // Use modern signal-based inputs and outputs
  planName = input.required<string>();
  daysCount = input<number>(0);
  selectPlan = output<void>();

  onSelect() {
    this.selectPlan.emit();
  }
}
```
