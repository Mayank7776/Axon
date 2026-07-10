import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Header } from '../header/header';
import { Footer } from '../footer/footer';

@Component({
  selector: 'app-main-body',
  imports: [RouterOutlet, Header, Footer],
  templateUrl: './main-body.html',
  styleUrl: './main-body.css',
})
export class MainBody {
}

