import { TestBed } from '@angular/core/testing';

import { EmailCopyService } from './email-copy.service';

describe('EmailCopyService', () => {
  let service: EmailCopyService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EmailCopyService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
