import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SocialMediaPostComponent } from './social-media-post.component';

describe('SocialMediaPostComponent', () => {
  let component: SocialMediaPostComponent;
  let fixture: ComponentFixture<SocialMediaPostComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SocialMediaPostComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SocialMediaPostComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
