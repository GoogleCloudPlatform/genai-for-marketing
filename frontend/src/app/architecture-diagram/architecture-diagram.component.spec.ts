import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ArchitectureDiagramComponent } from './architecture-diagram.component';

describe('ArchitectureDiagramComponent', () => {
  let component: ArchitectureDiagramComponent;
  let fixture: ComponentFixture<ArchitectureDiagramComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ArchitectureDiagramComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ArchitectureDiagramComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
