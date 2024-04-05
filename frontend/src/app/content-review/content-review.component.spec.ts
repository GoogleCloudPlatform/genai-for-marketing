import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContentReviewComponent } from './content-review.component';

describe('ContentReviewComponent', () => {
  let component: ContentReviewComponent;
  let fixture: ComponentFixture<ContentReviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ContentReviewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ContentReviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
