import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewWorkoutcard } from './view-workoutcard';

describe('ViewWorkoutcard', () => {
  let component: ViewWorkoutcard;
  let fixture: ComponentFixture<ViewWorkoutcard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewWorkoutcard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewWorkoutcard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
