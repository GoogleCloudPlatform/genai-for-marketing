import { Component } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { TrendspottingService } from '../services/trendspotting.service';
import { DatePipe } from '@angular/common';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CampaignService } from '../services/campaign.service';
import { LoginService } from '../services/login.service';
import { AudiencesService } from '../services/audiences.service';
export interface TableElement {
  email: string;
  total_transaction_value: number
}

export interface CampaignName {
  name: string
}

@Component({
  selector: 'app-trendspotting',
  templateUrl: './trendspotting.component.html',
  styleUrl: './trendspotting.component.scss'
})
export class TrendspottingComponent {
  showchatboot: boolean = false;
  topSearchedRank1: string = "";
  summarizeNewsResults: any;
  today!: Date;
  minDate!: Date;
  maxDate!: Date;
  onClickMarketingAssi() {
    this.showchatboot = true
  }
  trendspottingForm = new FormGroup({
    fromDate: new FormControl(),

  });
  summarizeNewsForm = new FormGroup({
    maxRecords: new FormControl(),
    keyword1: new FormControl(),
    keyword2: new FormControl(),
    keyword3: new FormControl(),
  });

  userLoggedIn: boolean = false;
  photoURL: string | undefined;
  eventsData: any;
  showCustomQuestion: boolean = false;
  showProgress: boolean = false;
  showData: boolean = false
  dropdownValue: any;
  genrateCode: any;
  audiencesEmails: any;
  total_transaction_value: any;
  queryData: any;
  CAMPAIGN_DATA: CampaignName[] = []
  userId: any;
  CampaignResults: any;
  filtered!: any;
  campaignId: any;
  campaignData: any;
  keyword1Value: string = 'Fashion'
  public query: string | undefined;
  campaignName: any
  constructor(public audiencesSerive: AudiencesService
    , public loginService: LoginService, public trendService: TrendspottingService, public datepipe: DatePipe, private snackBar: MatSnackBar,
    public campaignServ: CampaignService) {
    this.loginService.getUserDetails().subscribe(res => {
      this.userId = res?.uid
    });
  }
  onSubmit() {
    let date = this.trendspottingForm.controls.fromDate.value;
    let latest_date = this.datepipe.transform(date, 'yyyy-MM-dd');
    this.trendService.getTopSearchedTerms(latest_date).subscribe((res: any) => {
      this.topSearchedRank1 = res.top_search_terms[0]?.term
    })
  }

  initialValue: number = 3;
  step: number = 1;
  min: number = 1;
  max: number = 10;

  ngOnInit() {
    this.loginService.getUserDetails().subscribe(res => {
      this.userLoggedIn = true;
      this.photoURL = res?.photoURL;
      this.userId = res?.uid
    });
    let dateToday: Date = new Date();
    let dayBeforeYesterday: Date = new Date();
    dayBeforeYesterday = new Date(dateToday.setDate(dateToday.getDate() - 2));
    this.maxDate = dayBeforeYesterday;

    this.minDate = new Date(dateToday.setDate(dateToday.getDate() - 28));
    this.trendspottingForm.controls.fromDate.patchValue(dayBeforeYesterday)
    this.summarizeNewsForm.patchValue({
      maxRecords: 3,
    });
  }

  toggleMore() {
    if (this.summarizeNewsForm.controls.maxRecords.value < this.max) {
      this.summarizeNewsForm.controls.maxRecords.patchValue(this.summarizeNewsForm.controls.maxRecords.value + 1);
    }
  };

  toggleLess() {
    if (this.summarizeNewsForm.controls.maxRecords.value > this.min) {
      this.summarizeNewsForm.controls.maxRecords.patchValue(this.summarizeNewsForm.controls.maxRecords.value - 1);
    }
  };
  onSummarizeNewsSubmit() {
    this.showProgress = true;
    this.getCampaign();
    // let keyword1Value
    // if(this.summarizeNewsForm.controls.keyword1?.value === null){
    //   this.keyword1Value = 'Fashion';
    // } else{
    //   this.keyword1Value = this.summarizeNewsForm.controls.keyword1?.value;
    // }
    let keywords = []
    if (this.keyword1Value) {
      keywords.push(this.keyword1Value)
    }

    let keyword2Value = this.summarizeNewsForm.controls.keyword2?.value;
    if (keyword2Value) {
      keywords.push(keyword2Value)
    }

    let keyword3Value = this.summarizeNewsForm.controls.keyword3?.value;
    if (keyword3Value) {
      keywords.push(keyword3Value)
    }
    let obj = {
      "keywords": keywords,
      "max_records": this.summarizeNewsForm.controls.maxRecords?.value,
      "max_days": 30
    }
    this.trendService.postSummarizeNews(obj).subscribe((res: any) => {
      this.summarizeNewsResults = res?.summaries;
      this.showData = true;
      this.showProgress = false;
    })
  }

  getCampaign() {
    this.campaignServ.getCampaigns(this.userId).subscribe((res: any) => {
      this.CampaignResults = res.results;
      this.CAMPAIGN_DATA = this.CampaignResults?.map((res: any) => {
        return { name: res.data.name, id: res.id };
      })
      this.campaignId = this.CampaignResults[0].id;
      this.campaignName = this.CampaignResults[0].data.name;
    });
  }


  onClickCampaign(selectedValue: any) {
    this.campaignName = selectedValue;
    this.filtered = this.CampaignResults.filter((a: any) => a.data.name === selectedValue)
    this.filtered.forEach((element: { data: any; id: any, name: any }) => {
      this.campaignId = element.id;
      this.campaignData = element.data
    });
  }

  save() {
    let selectedCampaign = this.CampaignResults.filter((c: any) => c.id === this.campaignId);

    selectedCampaign[0].data.trendspotting_summaries = this.summarizeNewsResults
    let obj = {
      "name": selectedCampaign[0].data.name,
      "theme": selectedCampaign[0].data.theme,
      "brief": selectedCampaign[0].data.brief,
      "emails": selectedCampaign[0].data.emails,
      "website_post": selectedCampaign[0].data.website_post,
      "ads_threads": selectedCampaign[0].data.ads_threads,
      "ads_insta": selectedCampaign[0].data.ads_insta,
      "asset_classes_text": selectedCampaign[0].data.asset_classes_text,
      "asset_classes_images": selectedCampaign[0].data.asset_classes_images,
      "workspace_assets": selectedCampaign[0].data.workspace_assets,
      "trendspotting_summaries": selectedCampaign[0].data.trendspotting_summaries,
      "audiences": selectedCampaign[0].data.audiences,
      "campaign_uploaded_images": selectedCampaign[0].data.campaign_uploaded_images,
      "status": selectedCampaign[0].data.status
    }
    this.audiencesSerive.updateCampaign(obj, this.userId, this.campaignId).subscribe((res: any) => {
      this.showSnackbar(res?.message, 'Close', '4000')
    });
  }

  showSnackbar(content: any, action: any, duration: any) {
    let sb = this.snackBar.open(content, action, {
      duration: duration,
    });
    sb.onAction().subscribe(() => {
      sb.dismiss();
    });
  }
}
