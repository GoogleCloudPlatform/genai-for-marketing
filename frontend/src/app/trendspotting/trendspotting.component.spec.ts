import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrendspottingComponent } from './trendspotting.component';

describe('TrendspottingComponent', () => {
  let component: TrendspottingComponent;
  let fixture: ComponentFixture<TrendspottingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TrendspottingComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TrendspottingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
