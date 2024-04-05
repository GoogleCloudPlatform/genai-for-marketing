import { TestBed } from '@angular/core/testing';

import { ImageMaskService } from './image-mask.service';

describe('ImageMaskService', () => {
  let service: ImageMaskService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ImageMaskService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
