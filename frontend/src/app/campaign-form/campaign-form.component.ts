import { Component } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { CampaignService } from '../services/campaign.service';
import { LoginService } from '../services/login.service';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-campaign-form',
  templateUrl: './campaign-form.component.html',
  styleUrl: './campaign-form.component.scss'
})
export class CampaignFormComponent {
  userId: any;
  showchatboot: boolean = false;
  showProgress: boolean = false;
  userLoggedIn: boolean = false;
  photoURL: any;
  constructor(public campaignServ: CampaignService, public loginService: LoginService, private sanitizer: DomSanitizer) {
    this.loginService.getUserDetails().subscribe(res => {
      this.userId = res?.uid;
      this.userLoggedIn = true;
      this.photoURL = res?.photoURL;
    });
  }
  docPreviewUrl: any = ''
  campaignForm = new FormGroup({
    name: new FormControl(),
    theme: new FormControl(),
    otherTheme: new FormControl(),
    ageGroup: new FormControl(),
    gender: new FormControl(),
    goal: new FormControl(),
    competitor: new FormControl()
  });

  onSubmit() {
    let obj = {
      "campaign_name": this.campaignForm.controls["name"].value,
      "theme": this.campaignForm.controls["theme"].value,
      "brief": {
        "gender_select_theme": this.campaignForm.controls["gender"].value,
        "age_select_theme": this.campaignForm.controls["ageGroup"].value,
        "objective_select_theme": this.campaignForm.controls["goal"].value,
        "competitor_select_theme": this.campaignForm.controls["competitor"].value
      }
    }
    if (this.campaignForm.controls["theme"].value === 'Another theme...') {
      obj = {
        "campaign_name": this.campaignForm.controls["name"].value,
        "theme": this.campaignForm.controls["otherTheme"].value,
        "brief": {
          "gender_select_theme": this.campaignForm.controls["gender"].value,
          "age_select_theme": this.campaignForm.controls["ageGroup"].value,
          "objective_select_theme": this.campaignForm.controls["goal"].value,
          "competitor_select_theme": this.campaignForm.controls["competitor"].value
        }
      }
    }
    if (this.campaignForm.valid) {
      this.showProgress = true;
      this.campaignServ.createCampaign(obj, this.userId).subscribe((res: any) => {
        this.docPreviewUrl = `https://docs.google.com/file/d/${res?.workspace_assets?.doc_id}/preview`;
        this.showProgress = false;
        this.clear()
      });
    }
  }
  onClickMarketingAssi() {
    this.showchatboot = true
  }
  clear() {
    this.campaignForm.reset()
  }
}
