import { TestBed } from '@angular/core/testing';

import { Myworkout } from './myworkout';

describe('Myworkout', () => {
  let service: Myworkout;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Myworkout);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
