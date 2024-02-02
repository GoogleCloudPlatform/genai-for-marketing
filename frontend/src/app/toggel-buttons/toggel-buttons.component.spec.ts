import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ToggelButtonsComponent } from './toggel-buttons.component';

describe('ToggelButtonsComponent', () => {
  let component: ToggelButtonsComponent;
  let fixture: ComponentFixture<ToggelButtonsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ToggelButtonsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ToggelButtonsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
