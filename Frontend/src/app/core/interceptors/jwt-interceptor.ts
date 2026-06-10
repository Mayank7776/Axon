import { HttpInterceptorFn } from '@angular/common/http';

export const jwtInterceptor: HttpInterceptorFn = (req, next) => {

  const excludedUrls = [
    '/auth/login',
    '/auth/register',
    '/auth/forgot-password',
    '/auth/reset-password'
  ];

  const shouldSkip = excludedUrls.some(url =>
    req.url.includes(url)
  );

  if (shouldSkip) {
    return next(req);
  }

  const token = localStorage.getItem('accessToken');

  if (token) {
    req = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }

  return next(req);
};
