import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpsertWorkoutcard } from './upsert-workoutcard';

describe('UpsertWorkoutcard', () => {
  let component: UpsertWorkoutcard;
  let fixture: ComponentFixture<UpsertWorkoutcard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UpsertWorkoutcard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UpsertWorkoutcard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
