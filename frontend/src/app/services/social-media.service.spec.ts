import { TestBed } from '@angular/core/testing';

import { SocialMediaService } from './social-media.service';

describe('SocialMediaService', () => {
  let service: SocialMediaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SocialMediaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
