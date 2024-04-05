import { TestBed } from '@angular/core/testing';

import { TrendspottingService } from './trendspotting.service';

describe('TrendspottingService', () => {
  let service: TrendspottingService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TrendspottingService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
