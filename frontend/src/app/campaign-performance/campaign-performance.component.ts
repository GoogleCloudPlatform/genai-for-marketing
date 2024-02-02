import { Component } from '@angular/core';
import { LoginService } from '../services/login.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-campaign-performance',
  templateUrl: './campaign-performance.component.html',
  styleUrl: './campaign-performance.component.scss'
})
export class CampaignPerformanceComponent {
  userLoggedIn: boolean = false;
  showchatboot: boolean = false;
  overview: boolean = false
  photoURL: string | undefined;
  subscription: Subscription | undefined;
  selectedObject: any
  showOverview: any
  webTraffic: boolean = false
  storePerformance:boolean = false;
  campaignPerformance:boolean = false;
  campaignComparison:boolean = false;
  productPerformance:boolean = false;
  propensitytoPurchasePredictions:boolean = false;
  customerLifetimeValue:boolean = false;
  demandForecasting:boolean = false;
  sentimentAnalysis:boolean = false;
  audienceRegistry:boolean = false;
  productAvailabilityDetailedView:boolean = false;
  predictedUserLTVRevenueDetailedView:boolean = false;
  PurchasePredictionDetailedView:boolean = false;
  ProductDataDetailedView: boolean = false
  constructor( public loginService: LoginService) {
    this.subscription = this.loginService.getUserDetails().subscribe(res => {
      this.userLoggedIn = true;
      this.photoURL = res?.photoURL
    });
  }
  
  onClickMarketingAssi() {
    this.showchatboot = true
  }
  
  onClick(selectedValue : any) {
    if(selectedValue === 'Overview'){
     this.overview =true;
     this.webTraffic =false;
     this.storePerformance =false;
     this.campaignPerformance = false;
     this.campaignComparison = false;
     this.productPerformance =false;
     this.propensitytoPurchasePredictions =false;
     this.customerLifetimeValue =false;
     this.demandForecasting =false;
     this.sentimentAnalysis =false;
     this.audienceRegistry =false;
     this.productAvailabilityDetailedView =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.PurchasePredictionDetailedView =false;
     this.ProductDataDetailedView =false;
    } else if(selectedValue === 'Web Traffic'){
      this.overview =false;
      this.webTraffic =true;
     this.storePerformance =false;
     this.campaignPerformance = false;
     this.campaignComparison = false;
     this.productPerformance =false;
     this.propensitytoPurchasePredictions =false;
     this.customerLifetimeValue =false;
     this.demandForecasting =false;
     this.sentimentAnalysis =false;
     this.audienceRegistry =false;
     this.productAvailabilityDetailedView =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.PurchasePredictionDetailedView =false;
     this.ProductDataDetailedView =false;
    } else if(selectedValue === 'Store Performance'){
      this.storePerformance =true;
      this.overview =false;
      this.webTraffic =false;
     this.campaignPerformance = false;
     this.campaignComparison = false;
     this.productPerformance =false;
     this.propensitytoPurchasePredictions =false;
     this.customerLifetimeValue =false;
     this.demandForecasting =false;
     this.sentimentAnalysis =false;
     this.audienceRegistry =false;
     this.productAvailabilityDetailedView =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.PurchasePredictionDetailedView =false;
     this.ProductDataDetailedView =false;
    } else if(selectedValue === 'Campaign Performance'){
      this.campaignPerformance =true;
      this.overview =false;
      this.webTraffic =false;
     this.storePerformance =false;
     this.campaignComparison = false;
     this.productPerformance =false;
     this.propensitytoPurchasePredictions =false;
     this.customerLifetimeValue =false;
     this.demandForecasting =false;
     this.sentimentAnalysis =false;
     this.audienceRegistry =false;
     this.productAvailabilityDetailedView =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.PurchasePredictionDetailedView =false;
     this.ProductDataDetailedView =false;
    }
    else if(selectedValue === 'Campaign Comparison'){
      this.campaignComparison =true;
      this.overview =false;
      this.webTraffic =false;
     this.storePerformance =false;
     this.productPerformance =false;
     this.propensitytoPurchasePredictions =false;
     this.customerLifetimeValue =false;
     this.demandForecasting =false;
     this.sentimentAnalysis =false;
     this.audienceRegistry =false;
     this.productAvailabilityDetailedView =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.PurchasePredictionDetailedView =false;
     this.ProductDataDetailedView =false;
    }
    else if(selectedValue === 'Product Performance'){
      this.productPerformance =true;
      this.overview =false;
      this.webTraffic =false;
     this.storePerformance =false;
     this.campaignComparison = false;
     this.propensitytoPurchasePredictions =false;
     this.customerLifetimeValue =false;
     this.demandForecasting =false;
     this.sentimentAnalysis =false;
     this.audienceRegistry =false;
     this.productAvailabilityDetailedView =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.PurchasePredictionDetailedView =false;
     this.ProductDataDetailedView =false;
    }
    else if(selectedValue === 'Propensity to Purchase Predictions'){
      this.propensitytoPurchasePredictions =true;
      this.overview =false;
      this.webTraffic =false;
     this.storePerformance =false;
     this.campaignComparison = false;
     this.productPerformance =false;
     this.customerLifetimeValue =false;
     this.demandForecasting =false;
     this.sentimentAnalysis =false;
     this.audienceRegistry =false;
     this.productAvailabilityDetailedView =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.PurchasePredictionDetailedView =false;
     this.ProductDataDetailedView =false;
    }
    else if(selectedValue === 'Customer Lifetime Value'){
      this.customerLifetimeValue =true;
      this.overview =false;
      this.webTraffic =false;
     this.storePerformance =false;
     this.campaignComparison = false;
     this.productPerformance =false;
     this.propensitytoPurchasePredictions =false;
     this.demandForecasting =false;
     this.sentimentAnalysis =false;
     this.audienceRegistry =false;
     this.productAvailabilityDetailedView =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.PurchasePredictionDetailedView =false;
     this.ProductDataDetailedView =false;
    }
    else if(selectedValue === 'Demand Forecasting'){
      this.demandForecasting =true;
      this.overview =false;
      this.webTraffic =false;
     this.storePerformance =false;
     this.campaignComparison = false;
     this.productPerformance =false;
     this.propensitytoPurchasePredictions =false;
     this.customerLifetimeValue =false;
     this.sentimentAnalysis =false;
     this.audienceRegistry =false;
     this.productAvailabilityDetailedView =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.PurchasePredictionDetailedView =false;
     this.ProductDataDetailedView =false;
    }
    else if(selectedValue === 'Sentiment Analysis'){
      this.sentimentAnalysis =true;
      this.overview =false;
      this.webTraffic =false;
     this.storePerformance =false;
     this.campaignComparison = false;
     this.productPerformance =false;
     this.propensitytoPurchasePredictions =false;
     this.customerLifetimeValue =false;
     this.demandForecasting =false;
     this.audienceRegistry =false;
     this.productAvailabilityDetailedView =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.PurchasePredictionDetailedView =false;
     this.ProductDataDetailedView =false;
    }
    else if(selectedValue === 'Audience Registry'){
      this.audienceRegistry =true;
      this.overview =false;
      this.webTraffic =false;
     this.storePerformance =false;
     this.campaignComparison = false;
     this.productPerformance =false;
     this.propensitytoPurchasePredictions =false;
     this.customerLifetimeValue =false;
     this.demandForecasting =false;
     this.sentimentAnalysis =false;
     this.productAvailabilityDetailedView =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.PurchasePredictionDetailedView =false;
     this.ProductDataDetailedView =false;
    }
    else if(selectedValue === 'Product Availability-Detailed View'){
      this.productAvailabilityDetailedView =true;
      this.overview =false;
      this.webTraffic =false;
     this.storePerformance =false;
     this.campaignComparison = false;
     this.productPerformance =false;
     this.propensitytoPurchasePredictions =false;
     this.customerLifetimeValue =false;
     this.demandForecasting =false;
     this.sentimentAnalysis =false;
     this.audienceRegistry =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.PurchasePredictionDetailedView =false;
     this.ProductDataDetailedView =false;
    }
    else if(selectedValue === 'Predicted User LTV Revenue-Detailed View'){
      this.predictedUserLTVRevenueDetailedView =true;
      this.overview =false;
      this.webTraffic =false;
     this.storePerformance =false;
     this.campaignComparison = false;
     this.productPerformance =false;
     this.propensitytoPurchasePredictions =false;
     this.customerLifetimeValue =false;
     this.demandForecasting =false;
     this.sentimentAnalysis =false;
     this.audienceRegistry =false;
     this.productAvailabilityDetailedView =false;
     this.PurchasePredictionDetailedView =false;
     this.ProductDataDetailedView =false;
    }
    else if(selectedValue === 'Purchase Prediction-Detailed View'){
      this.PurchasePredictionDetailedView =true;
      this.overview =false;
      this.webTraffic =false;
     this.storePerformance =false;
     this.campaignComparison = false;
     this.productPerformance =false;
     this.propensitytoPurchasePredictions =false;
     this.customerLifetimeValue =false;
     this.demandForecasting =false;
     this.sentimentAnalysis =false;
     this.audienceRegistry =false;
     this.productAvailabilityDetailedView =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.ProductDataDetailedView =false;
    }
    else if(selectedValue === 'Product Data-Detailed View'){
      this.ProductDataDetailedView =true;
      this.overview =false;
      this.webTraffic =false;
     this.storePerformance =false;
     this.campaignComparison = false;
     this.productPerformance =false;
     this.propensitytoPurchasePredictions =false;
     this.customerLifetimeValue =false;
     this.demandForecasting =false;
     this.sentimentAnalysis =false;
     this.audienceRegistry =false;
     this.productAvailabilityDetailedView =false;
     this.predictedUserLTVRevenueDetailedView =false;
     this.PurchasePredictionDetailedView =false;
    }

  }
}
