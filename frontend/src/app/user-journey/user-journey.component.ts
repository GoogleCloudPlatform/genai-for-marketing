import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-user-journey',
  templateUrl: './user-journey.component.html',
  styleUrl: './user-journey.component.scss'
})
export class UserJourneyComponent {
  photoURL: string | undefined;
  subscription: Subscription | undefined;
  constructor(public _router: Router, public loginService: LoginService) {
    this.subscription = this.loginService.getUserDetails().subscribe(message => {
      this.photoURL = message?.photoURL
    });
  }
  ngOnInit() { }

  userJourneyList: any = [{
    userId: "User journey 1",
    userImg: "assets/Persona headshots/Marla.png",
    userTitle: "Marketing Analyst",
    userContent: [
      "Derive marketing insights from past campaigns.",
      "Data integration and visualization with Looker",
      "Explore and segment audiences.",
      "Identify trends in current and historical data and news.",
      "Perform research against internal data."
    ]
  },
  {
    userId: "User journey 2",
    userImg: "assets/Persona headshots/Firefly professional headshot of african american man 82343.jpg",
    userTitle: "Content Creator",
    userContent: [
      "Generate emails and associated images for customer segments",
      "Generate website post and associated images",
      "Generate social media post types",
      "Generate Google Ads asset groups"
    ]
  },
  {
    userId: "User journey 3",
    userImg: "assets/Persona headshots/Customer Experience Analyst.png",
    userTitle: "Campaign Manager",
    userContent: [
      "Campaign brief creation",
      "Data integration and visualization with Looker",
      "Connection with external data sources (CDP, GA4, Google Ads)",
      "Campaign Activation"
    ]
  }
  ];

  greyOutUserJourneyList = [
    {
      userId: "User journey 2",
      userImg: "assets/Persona headshots/Firefly professional headshot of african american man 82343.jpg",
      userTitle: "Content Creator",
      userContent: [
        "Generate emails and associated images for customer segments",
        "Generate website post and associated images",
        "Generate social media post types",
        "Generate Google Ads asset groups"
      ]
    },
    {
      userId: "User journey 3",
      userImg: "assets/Persona headshots/Customer Experience Analyst.png",
      userTitle: "Campaign Manager",
      userContent: [
        "Campaign brief creation",
        "Data integration and visualization with Looker",
        "Connection with external data sources (CDP, GA4, Google Ads)",
        "Campaign Activation"
      ]
    },
    {
      userId: "User journey 4",
      userImg: "assets/Persona headshots/Firefly headshot of ugly italian man 82343.jpg",
      userTitle: "Customer Service Agent",
      userContent: [
        "Search capability for internal knowledge bases and external references",
        "Response for customers inquiries with citations (grounding)",
        "Summarize historical conversations to enhance customer experience"
      ]
    },
    {
      userId: "User journey 5",
      userImg: "assets/Persona headshots/Field Service Agent.jpg",
      userTitle: "Customer Service Agent",
      userContent: [
        "Contact center agent performance analytics",
        "Data integration and visualization with Looker",
        "Connection with external data sources (CDP, GA4, Google Ads)",
        "Campaign Activation"
      ]
    }
  ]
  navigateToHome() {
    this._router.navigate(['home'])
  }
}
