import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WatchWorkout } from './watch-workout';

describe('WatchWorkout', () => {
  let component: WatchWorkout;
  let fixture: ComponentFixture<WatchWorkout>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WatchWorkout]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WatchWorkout);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
