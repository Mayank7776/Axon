import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Addchat } from './addchat';

describe('Addchat', () => {
  let component: Addchat;
  let fixture: ComponentFixture<Addchat>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Addchat]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Addchat);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
