import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WebsitePostComponent } from './website-post.component';

describe('WebsitePostComponent', () => {
  let component: WebsitePostComponent;
  let fixture: ComponentFixture<WebsitePostComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [WebsitePostComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(WebsitePostComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
