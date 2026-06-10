import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewNutritionPlan } from './view-nutrition-plan';

describe('ViewNutritionPlan', () => {
  let component: ViewNutritionPlan;
  let fixture: ComponentFixture<ViewNutritionPlan>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewNutritionPlan]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewNutritionPlan);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
