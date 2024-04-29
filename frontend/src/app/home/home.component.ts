import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { LoginService } from '../services/login.service';
import { environment } from '../../environments/environments';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss',
})
export class HomeComponent {
  photoURL: string | undefined;
  subscription: Subscription | undefined;
  showCampaignform: boolean = false;
  showchatboot: boolean = false;
  showMarketingInsightPage: boolean = false;
  showCampaignPerformace: boolean = false;
  showHomePage: boolean = true;
  showMainContent: boolean = true;
  showExistingCampaigns: boolean = false;
  showAudiences: boolean = false;
  showTrendspotting: boolean = false;
  showConsumerInsights: boolean = false
  showEmailCopy: boolean = false
  showSocialMedia: boolean = false;
  showWebsitePost: boolean = false;
  showAssestGroup: boolean = false;
  showContentReview: boolean = false;
  dialogflowCxAgendId: string | undefined;
  userProjectId: string | undefined;

  constructor(public _router: Router, public loginService: LoginService) {
    this.subscription = this.loginService.getUserDetails().subscribe(message => {
      this.photoURL = message?.photoURL
    });
    this.dialogflowCxAgendId = environment.dialogflowCxAgendId;
    this.userProjectId = environment.firebaseConfig.projectId;
  }
  ngOnInit() {}

  onClickMarketingAssi() {
    this.showchatboot = true
  }

  naviagteToMarketingInsights() {
    //this._router.navigate(['marketing-insights'])
    this.showMarketingInsightPage = true;
    this.showMainContent = false
    this.showCampaignPerformace = false;
    this.showCampaignform = false;
    this.showExistingCampaigns = false;
    this.showAudiences = false;
    this.showConsumerInsights = false;
    this.showEmailCopy = false
    this.showTrendspotting = false;
    this.showSocialMedia = false;
    this.showWebsitePost = false;
    this.showAssestGroup = false;
    this.showContentReview = false;
  }

  naviagteToHomePgae() {
    this.showMainContent = true
    this.showCampaignPerformace = false;
    this.showCampaignform = false;
    this.showExistingCampaigns = false;
    this.showMarketingInsightPage = false;
    this.showAudiences = false;
    this.showConsumerInsights = false;
    this.showTrendspotting = false;
    this.showEmailCopy = false
    this.showSocialMedia = false;
    this.showWebsitePost = false;
    this.showAssestGroup = false;
    this.showContentReview = false;
  }

  startCampaign() {
    this.showCampaignform = true;
    this.showMainContent = false;
    this.showCampaignPerformace = false;
    this.showMarketingInsightPage = false;
    this.showExistingCampaigns = false;
    this.showAudiences = false;
    this.showTrendspotting = false;
    this.showConsumerInsights = false;
    this.showEmailCopy = false
    this.showSocialMedia = false;
    this.showWebsitePost = false;
    this.showAssestGroup = false;
    this.showContentReview = false;
  }

  existingCampaigns() {
    this.showCampaignform = false;
    this.showMainContent = false;
    this.showExistingCampaigns = true;
    this.showCampaignPerformace = false;
    this.showMarketingInsightPage = false;
    this.showAudiences = false;
    this.showTrendspotting = false;
    this.showConsumerInsights = false;
    this.showEmailCopy = false;
    this.showSocialMedia = false;
    this.showWebsitePost = false;
    this.showAssestGroup = false;
    this.showContentReview = false;
  }

  naviagteToCampaignPerformancPgae() {
    this.showCampaignPerformace = true;
    this.showMainContent = false
    this.showCampaignform = false;
    this.showExistingCampaigns = false;
    this.showMarketingInsightPage = false;
    this.showAudiences = false;
    this.showTrendspotting = false;
    this.showConsumerInsights = false;
    this.showEmailCopy = false;
    this.showSocialMedia = false
    this.showWebsitePost = false;
    this.showAssestGroup = false;
    this.showContentReview = false;
  }

  naviagteToAudiencesPgae() {
    this.showAudiences = true;
    this.showCampaignPerformace = false;
    this.showMainContent = false
    this.showCampaignform = false;
    this.showExistingCampaigns = false;
    this.showMarketingInsightPage = false;
    this.showTrendspotting = false;
    this.showEmailCopy = false
    this.showConsumerInsights = false;
    this.showSocialMedia = false
    this.showWebsitePost = false;
    this.showAssestGroup = false;
    this.showContentReview = false;
  }
  navigateToTrendspotting() {
    this.showAudiences = false;
    this.showCampaignPerformace = false;
    this.showMainContent = false
    this.showCampaignform = false;
    this.showExistingCampaigns = false;
    this.showMarketingInsightPage = false;
    this.showTrendspotting = true;
    this.showConsumerInsights = false;
    this.showEmailCopy = false;
    this.showSocialMedia = false
    this.showWebsitePost = false;
    this.showAssestGroup = false;
    this.showContentReview = false;
  }
  navigateToConsumerInsights() {
    this.showAudiences = false;
    this.showCampaignPerformace = false;
    this.showMainContent = false
    this.showCampaignform = false;
    this.showExistingCampaigns = false;
    this.showMarketingInsightPage = false;
    this.showTrendspotting = false;
    this.showConsumerInsights = true;
    this.showEmailCopy = false;
    this.showSocialMedia = false
    this.showWebsitePost = false;
    this.showAssestGroup = false;
    this.showContentReview = false;
  }

  emailCopy() {
    this.showEmailCopy = true
    this.showAudiences = false;
    this.showCampaignPerformace = false;
    this.showMainContent = false
    this.showCampaignform = false;
    this.showExistingCampaigns = false;
    this.showMarketingInsightPage = false;
    this.showTrendspotting = false;
    this.showConsumerInsights = false;
    this.showSocialMedia = false
    this.showWebsitePost = false;
    this.showAssestGroup = false;
    this.showContentReview = false;
  }
  socialMedia() {
    this.showEmailCopy = false
    this.showAudiences = false;
    this.showCampaignPerformace = false;
    this.showMainContent = false
    this.showCampaignform = false;
    this.showExistingCampaigns = false;
    this.showMarketingInsightPage = false;
    this.showTrendspotting = false;
    this.showConsumerInsights = false;
    this.showSocialMedia = true
    this.showWebsitePost = false;
    this.showAssestGroup = false;
    this.showContentReview = false;
  }

  onClickWebsitePost() {
    this.showWebsitePost = true
    this.showEmailCopy = false
    this.showAudiences = false;
    this.showCampaignPerformace = false;
    this.showMainContent = false
    this.showCampaignform = false;
    this.showExistingCampaigns = false;
    this.showMarketingInsightPage = false;
    this.showTrendspotting = false;
    this.showConsumerInsights = false;
    this.showSocialMedia = false
    this.showContentReview = false;
    this.showAssestGroup = false;
  }


  assetGroupPmax() {
    this.showWebsitePost = false
    this.showEmailCopy = false
    this.showAudiences = false;
    this.showCampaignPerformace = false;
    this.showMainContent = false
    this.showCampaignform = false;
    this.showExistingCampaigns = false;
    this.showMarketingInsightPage = false;
    this.showTrendspotting = false;
    this.showConsumerInsights = false;
    this.showSocialMedia = false;
    this.showAssestGroup = true;
    this.showContentReview = false;
  }
  navigateToContentReview() {

    this.showWebsitePost = false
    this.showEmailCopy = false
    this.showAudiences = false;
    this.showCampaignPerformace = false;
    this.showMainContent = false
    this.showCampaignform = false;
    this.showExistingCampaigns = false;
    this.showMarketingInsightPage = false;
    this.showTrendspotting = false;
    this.showConsumerInsights = false;
    this.showSocialMedia = false;
    this.showAssestGroup = false;
    this.showContentReview = true;
  }
}
