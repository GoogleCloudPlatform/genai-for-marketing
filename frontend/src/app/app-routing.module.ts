import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CampaignFormComponent } from './campaign-form/campaign-form.component';
import { LoginComponent } from './login/login.component';
import { UserJourneyComponent } from './user-journey/user-journey.component';
import { HomeComponent } from './home/home.component';
import { MarketingInsightsComponent } from './marketing-insights/marketing-insights.component';

const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'campaign-form' , component:CampaignFormComponent},
  { path: 'user-journey', component: UserJourneyComponent },
  { path: 'home', component: HomeComponent },
  { path: 'marketing-insights', component: MarketingInsightsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
