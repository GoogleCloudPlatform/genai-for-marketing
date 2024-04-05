import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CampaignListComponent } from './campaign-list.component';

describe('CampaignListComponent', () => {
  let component: CampaignListComponent;
  let fixture: ComponentFixture<CampaignListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CampaignListComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CampaignListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
