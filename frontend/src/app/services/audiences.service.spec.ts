import { TestBed } from '@angular/core/testing';

import { AudiencesService } from './audiences.service';

describe('AudiencesService', () => {
  let service: AudiencesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AudiencesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
