import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CampaignPerformanceComponent } from './campaign-performance.component';

describe('CampaignPerformanceComponent', () => {
  let component: CampaignPerformanceComponent;
  let fixture: ComponentFixture<CampaignPerformanceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CampaignPerformanceComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CampaignPerformanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
