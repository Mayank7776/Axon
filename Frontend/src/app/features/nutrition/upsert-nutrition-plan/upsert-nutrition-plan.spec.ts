import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpsertNutritionPlan } from './upsert-nutrition-plan';

describe('UpsertNutritionPlan', () => {
  let component: UpsertNutritionPlan;
  let fixture: ComponentFixture<UpsertNutritionPlan>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UpsertNutritionPlan]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UpsertNutritionPlan);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
