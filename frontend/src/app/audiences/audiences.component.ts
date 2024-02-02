import { AfterContentChecked, AfterContentInit, AfterViewChecked, AfterViewInit, Component, ElementRef, ViewChild, ViewChildren } from '@angular/core';
import { LoginService } from '../services/login.service';
import { Subscription } from 'rxjs';
import { SelectionModel } from '@angular/cdk/collections';
import { AudiencesService } from '../services/audiences.service';
import { Audience } from './audience';
import { CampaignService } from '../services/campaign.service';
import lodash, * as _ from 'lodash';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CdkVirtualScrollViewport } from '@angular/cdk/scrolling';
export interface TableElement {
  email: string;
  total_transaction_value: number
}

export interface Email {
  email: string;
}

export interface CampaignName {
  name: string
}
@Component({
  selector: 'app-audiences',
  templateUrl: './audiences.component.html',
  styleUrl: './audiences.component.scss'
})
export class AudiencesComponent implements AfterViewInit {
  @ViewChild("audienceRes")
  private audienceResDataDiv!: ElementRef<HTMLElement>;

  userLoggedIn: boolean = false;
  showchatboot: boolean = false;
  photoURL: string | undefined;
  subscription: Subscription | undefined;
  showTables: boolean = false;
  //audience: Audience[] | undefined;
  audiences: any
  eventsData: any;
  transactionsData: any
  data: [] | undefined;
  everntData: any
  showCustomQuestion: boolean = false;
  showProgress: boolean = false;
  showData: boolean = false
  dropdownValue: any;
  genrateCode: any;
  audiencesEmails: any;
  total_transaction_value: any;
  queryData: any;
  ELEMENT_DATA: TableElement[] = [];
  CAMPAIGN_DATA: CampaignName[] = []
  email: Email[] = []
  CAMPAIGN_DATA1: any[] = [];
  audiencesEmailsandtrasctionData: any;
  userId: any;
  CampaignResults: any;
  filtered!: any;
  dataCampaign: any;
  id: any;
  campaignData: any;
  public query: string | undefined;
  showProgressPreviewTable: boolean = false
  campaignId: any;
  audiencesData: any;
  visibleColumns: any[] | undefined;
  _alldata!: any[];
  displayedColumns = ['email', 'total_value'];
  dataSource: any;
  campaignName: any;
  showSaveButton: boolean = false;
  audienceResData: any[] = [];
  otherTheme = '';
  panelOpenState = false;
  promptResponse: any;

  constructor(public loginService: LoginService,
    public audiencesSerive: AudiencesService, private snackBar: MatSnackBar,
    public campaignServ: CampaignService) {
    this.subscription = this.loginService.getUserDetails().subscribe(res => {
      this.userLoggedIn = true;
      this.photoURL = res?.photoURL;
      this.userId = res?.uid
    });
  }
  ngOnInit() {
    this.getCampaign();
  }

  onClickMarketingAssi() {
    this.showchatboot = true
  }

  onClickPreviewTable() {
    this.showTables = true;
    this.getPreviewData();
    this.getPreviewTableDataEvents();
    this.getPreviewTableDataTransactions();
  }

  getPreviewData() {
    this.showProgressPreviewTable = true
    this.audiencesSerive.getPreviewTableData().subscribe((res: any) => {
      //this.audiences = res.table_sample;
      this.audiences = res.data;
      this.showProgressPreviewTable = false
    });
  }

  getPreviewTableDataEvents() {
    this.showProgressPreviewTable = true
    this.audiencesSerive.getPreviewTableDataEvents().subscribe((res: any) => {
      //this.everntData = res.table_sample
      this.eventsData = res.data;
      this.showProgressPreviewTable = false
    });
  }

  getPreviewTableDataTransactions() {
    this.showProgressPreviewTable = true
    this.audiencesSerive.getPreviewTableDataTransactions().subscribe((res: any) => {
      //this.everntData = res.table_sample
      this.transactionsData = res.data;
      this.showProgressPreviewTable = false
    });
  }

  onClick(selectedValue: any) {
    this.dropdownValue = selectedValue
    if (selectedValue === 'Another question...') {
      this.showCustomQuestion = true;
    } else {
      this.showCustomQuestion = false;
    }
  }

  generate() {
    if (this.showCustomQuestion) {
      this.dropdownValue = this.otherTheme
    }
    this.showProgress = true
    this.audiencesSerive.generateQuery(this.dropdownValue).subscribe((res: any) => {
      this.genrateCode = res.gen_code;
      this.promptResponse = res.prompt;
      this.audiencesEmailsandtrasctionData = res.audiences.crm_data;
      this.audienceResData = res.audiences.data
      this.dataSource = res.audiences.crm_data; //email,city,age_group,gender,first_name
      this.showData = true
      this.showProgress = false
      this.audiencesData = res.audiences;
      this.ngAfterViewInit();
    });
    //this.getAudiencesEmailsandtrasctionData();
  }

  // ngAfterContentChecked() {
  //   this.audienceResDataDiv!?.nativeElement?.scrollIntoView({
  //     behavior: "smooth",
  //     block: "start",
  //     inline: "nearest"
  //   });
  // }
  ngAfterViewInit() {
    this.audienceResDataDiv!?.nativeElement?.scrollIntoView({
      behavior: "smooth",
      block: "start",
      inline: "nearest"
    });
  }

  getAudiencesEmailsandtrasctionData() {
    this.audiencesSerive.getaudienceTableData().subscribe((res: any) => {
      this.audiencesEmailsandtrasctionData = res.audiences
    });
  }
  showContentCopiedMsg(){
    this.showSnackbarCssStyles("Content Copied", 'Close', '4000')
  }
  getCampaign() {
    this.campaignServ.getCampaigns(this.userId).subscribe((res: any) => {
      this.CampaignResults = res.results;
      this.CAMPAIGN_DATA1 = res.results;
      this.CAMPAIGN_DATA = this.CampaignResults?.map((res: any) => {
        return { name: res.data.name, id: res.id };
      })
      this.campaignId = this.CampaignResults[0].id;
    });
  }


  onClickCampaign(selectedValue: any) {
    this.campaignName = selectedValue;
    this.showSaveButton = true
    this.filtered = this.CAMPAIGN_DATA1.filter(a => a.data.name === selectedValue)
    // this.id = this.filtered.id;
    // this.campaignData = this.filtered.data
    this.filtered.forEach((element: { data: any; id: any }) => {
      this.campaignId = element.id;
      this.campaignData = element.data
    });

  }



  save() {
    let selectedCampaign = this.CampaignResults.filter((c: any) => c.id === this.campaignId);
    selectedCampaign[0].data.audiences = this.audiencesData
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
      this.showSnackbarCssStyles(res?.message, 'Close', '4000')
    });
  }

  showSnackbarCssStyles(content: any, action: any, duration: any) {
    let sb = this.snackBar.open(content, action, {
      duration: duration,
      panelClass: ["custom-style"]
    });
    sb.onAction().subscribe(() => {
      sb.dismiss();
    });
  }

}

