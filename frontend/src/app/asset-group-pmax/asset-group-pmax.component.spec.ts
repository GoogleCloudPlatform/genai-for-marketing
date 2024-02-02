import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AssetGroupPmaxComponent } from './asset-group-pmax.component';

describe('AssetGroupPmaxComponent', () => {
  let component: AssetGroupPmaxComponent;
  let fixture: ComponentFixture<AssetGroupPmaxComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AssetGroupPmaxComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AssetGroupPmaxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
