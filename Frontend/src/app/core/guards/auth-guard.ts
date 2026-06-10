import { CanActivateFn, Router } from '@angular/router';
import { Auth } from '../../services/auth';
import { inject } from '@angular/core/primitives/di';
import { catchError, map, of } from 'rxjs';

export const authGuard: CanActivateFn = (route, state) => {
  const auth = inject(Auth);
  const router = inject(Router);

  const token = localStorage.getItem('accessToken');

  if (!token) {
    router.navigate(['/login']);
    return false;
  }

  return auth.validateToken().pipe(
    map(() => true),
    catchError(() => {
      localStorage.clear();
      router.navigate(['/login']);
      return of(false);
    })
  );
};
