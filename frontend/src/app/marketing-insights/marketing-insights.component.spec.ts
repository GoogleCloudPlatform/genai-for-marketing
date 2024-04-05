import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MarketingInsightsComponent } from './marketing-insights.component';

describe('MarketingInsightsComponent', () => {
  let component: MarketingInsightsComponent;
  let fixture: ComponentFixture<MarketingInsightsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MarketingInsightsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MarketingInsightsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
