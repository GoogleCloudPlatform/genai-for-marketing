import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExistingCampaignsComponent } from './existing-campaigns.component';

describe('ExistingCampaignsComponent', () => {
  let component: ExistingCampaignsComponent;
  let fixture: ComponentFixture<ExistingCampaignsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ExistingCampaignsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ExistingCampaignsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
