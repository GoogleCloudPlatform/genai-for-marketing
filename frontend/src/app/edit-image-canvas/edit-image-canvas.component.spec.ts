import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditImageCanvasComponent } from './edit-image-canvas.component';

describe('EditImageCanvasComponent', () => {
  let component: EditImageCanvasComponent;
  let fixture: ComponentFixture<EditImageCanvasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EditImageCanvasComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EditImageCanvasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
