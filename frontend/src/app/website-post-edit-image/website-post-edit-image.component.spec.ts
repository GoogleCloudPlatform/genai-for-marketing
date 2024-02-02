import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WebsitePostEditImageComponent } from './website-post-edit-image.component';

describe('WebsitePostEditImageComponent', () => {
  let component: WebsitePostEditImageComponent;
  let fixture: ComponentFixture<WebsitePostEditImageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [WebsitePostEditImageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(WebsitePostEditImageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
