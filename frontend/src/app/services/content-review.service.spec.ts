import { TestBed } from '@angular/core/testing';

import { ContentReviewService } from './content-review.service';

describe('ContentReviewService', () => {
  let service: ContentReviewService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ContentReviewService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
