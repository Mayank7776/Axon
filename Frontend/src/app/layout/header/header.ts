import { Component, signal } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { Sidebar } from '../sidebar/sidebar';

@Component({
  selector: 'app-header',
  imports: [RouterLink, RouterLinkActive, Sidebar],
  templateUrl: './header.html',
  styleUrl: './header.css',
})
export class Header {
  protected readonly isProfileDropdownOpen = signal(false);
  protected readonly isNotificationsOpen = signal(false);
  protected readonly isMobileMenuOpen = signal(false);

  toggleProfileDropdown() {
    this.isProfileDropdownOpen.update(v => !v);
    if (this.isProfileDropdownOpen()) {
      this.isNotificationsOpen.set(false);
      this.isMobileMenuOpen.set(false);
    }
  }

  toggleNotifications() {
    this.isNotificationsOpen.update(v => !v);
    if (this.isNotificationsOpen()) {
      this.isProfileDropdownOpen.set(false);
      this.isMobileMenuOpen.set(false);
    }
  }

  toggleMobileMenu() {
    this.isMobileMenuOpen.update(v => !v);
    if (this.isMobileMenuOpen()) {
      this.isProfileDropdownOpen.set(false);
      this.isNotificationsOpen.set(false);
    }
  }

  closeMobileMenu() {
    this.isMobileMenuOpen.set(false);
  }
}

