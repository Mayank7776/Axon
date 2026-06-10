import { inject } from '@angular/core/primitives/di';
import { CanActivateFn, Router } from '@angular/router';
import { Auth } from '../../services/auth';

export const guestGuard: CanActivateFn = (route, state) => {
  const auth = inject(Auth);
  const router = inject(Router);
  if (auth.validateToken()) {
    router.navigate(['/dashboard']);
    return false;
  }

  return true;
};

