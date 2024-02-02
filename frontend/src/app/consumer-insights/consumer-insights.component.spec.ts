import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsumerInsightsComponent } from './consumer-insights.component';

describe('ConsumerInsightsComponent', () => {
  let component: ConsumerInsightsComponent;
  let fixture: ComponentFixture<ConsumerInsightsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ConsumerInsightsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ConsumerInsightsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
