import { Component } from '@angular/core';
import { LoginService } from '../services/login.service';
import { FormGroup, FormControl } from '@angular/forms';
import { TrendspottingService } from '../services/trendspotting.service';

@Component({
  selector: 'app-consumer-insights',
  templateUrl: './consumer-insights.component.html',
  styleUrl: './consumer-insights.component.scss'
})
export class ConsumerInsightsComponent {
  userLoggedIn: boolean = false;
  showchatboot: boolean = false;
  photoURL: any;
  generateSuccessMsg: boolean = false;
  insightResults: any[] = [];
  llm_summary: any;
  constructor(public loginService: LoginService, public trendsService: TrendspottingService) {
    this.loginService.getUserDetails().subscribe(res => {
      this.userLoggedIn = true;
      this.photoURL = res?.photoURL
    });
  }
  insightsForm = new FormGroup({
    name: new FormControl(),
  });

  onClickMarketingAssi() {
    this.showchatboot = true
  }

  onSubmit() {
    let obj = {
      query: this.insightsForm.controls.name?.value
    }
    this.trendsService.consumerInsightsSearch(obj).subscribe((res: any) => {
      this.generateSuccessMsg = true;
      this.insightResults = res?.results;
      this.llm_summary = res?.llm_summary;
      if (res?.llm_summary.includes('not enough information') ){
        this.llm_summary = 'Generative summary not available this time.'
      }
    })
  }
}
