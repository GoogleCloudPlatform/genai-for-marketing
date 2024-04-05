import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SocialMediaEditCanvasComponent } from './social-media-edit-canvas.component';

describe('SocialMediaEditCanvasComponent', () => {
  let component: SocialMediaEditCanvasComponent;
  let fixture: ComponentFixture<SocialMediaEditCanvasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SocialMediaEditCanvasComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(SocialMediaEditCanvasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
