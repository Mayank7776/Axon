import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth-guard';
import { guestGuard } from './core/guards/guest-guard';

export const routes: Routes = [
    {
     path: 'login',
     loadComponent: () => import("./auth/login/login").then(m => m.Login),
     // canActivate: [guestGuard]
    },
    {
     path :'',
     loadComponent: () => import("./layout/main-body/main-body").then(m => m.MainBody),
     // canActivate: [authGuard],
     children : [
        {
          path: '',
          redirectTo: 'home',
          pathMatch: 'full'
        },
        {
         path:'home',
         loadComponent: () => import("./features/home/home").then(m => m.Home)
        },
        {
         path:'workouts',
         loadComponent: () => import("./features/workouts/workouts").then(m => m.Workouts)
        },
        {
         path:'progress',
         loadComponent: () => import("./features/progress/progress").then(m => m.Progress)
        },
        {
         path:'chat',
         loadComponent: () => import("./features/chat/chat").then(m => m.Chat)
        },
        {
         path:'blog',
         loadComponent: () => import("./features/blog/blog").then(m => m.Blog)
        }
     ]
    },
    {
      path: '404',
      loadComponent: () =>
        import('./features/errorpage/errorpage')
          .then(m => m.Errorpage)
    },
    {
      path: '**',
      redirectTo: '404'
    }
];
