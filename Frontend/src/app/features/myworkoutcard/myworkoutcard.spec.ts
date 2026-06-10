import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Myworkoutcard } from './myworkoutcard';

describe('Myworkoutcard', () => {
  let component: Myworkoutcard;
  let fixture: ComponentFixture<Myworkoutcard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Myworkoutcard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Myworkoutcard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
