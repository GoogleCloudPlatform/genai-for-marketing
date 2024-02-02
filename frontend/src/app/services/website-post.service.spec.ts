import { TestBed } from '@angular/core/testing';

import { WebsitePostService } from './website-post.service';

describe('WebsitePostService', () => {
  let service: WebsitePostService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(WebsitePostService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
