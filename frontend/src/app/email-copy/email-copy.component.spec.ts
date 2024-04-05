import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EmailCopyComponent } from './email-copy.component';

describe('EmailCopyComponent', () => {
  let component: EmailCopyComponent;
  let fixture: ComponentFixture<EmailCopyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EmailCopyComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(EmailCopyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
