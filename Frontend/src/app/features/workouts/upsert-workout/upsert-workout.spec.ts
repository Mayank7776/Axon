import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpsertWorkout } from './upsert-workout';

describe('UpsertWorkout', () => {
  let component: UpsertWorkout;
  let fixture: ComponentFixture<UpsertWorkout>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UpsertWorkout]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UpsertWorkout);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
