import { TestBed } from '@angular/core/testing';

import { AssetGroupPmaxService } from './asset-group-pmax.service';

describe('AssetGroupPmaxService', () => {
  let service: AssetGroupPmaxService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AssetGroupPmaxService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
