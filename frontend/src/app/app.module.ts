import { CUSTOM_ELEMENTS_SCHEMA, NgModule, importProvidersFrom } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';
import { DialogModule } from '@angular/cdk/dialog';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { CampaignFormComponent } from './campaign-form/campaign-form.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LoginComponent } from './login/login.component';
import { LoginButtonComponent } from './login-button/login-button.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { provideFirebaseApp, initializeApp } from '@angular/fire/app';
import { getFirestore, provideFirestore } from '@angular/fire/firestore';
import { UserJourneyComponent } from './user-journey/user-journey.component';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { ToggelButtonsComponent } from './toggel-buttons/toggel-buttons.component';
import { ArchitectureDiagramComponent } from './architecture-diagram/architecture-diagram.component';
import { HttpClientModule } from '@angular/common/http';
import { CampaignListComponent } from './campaign-list/campaign-list.component';
import { MaterialModule } from './material/material.module';
import { NgxDocViewerModule } from 'ngx-doc-viewer';


import { MarketingInsightsComponent } from './marketing-insights/marketing-insights.component';
import { CampaignPerformanceComponent } from './campaign-performance/campaign-performance.component';
import { ExistingCampaignsComponent } from './existing-campaigns/existing-campaigns.component';

import { CustomerService } from '../app/customer.service';

import { TableModule } from 'primeng/table';
import { CalendarModule } from 'primeng/calendar';
import { SliderModule } from 'primeng/slider';
import { MultiSelectModule } from 'primeng/multiselect';
import { ContextMenuModule } from 'primeng/contextmenu';
import { ButtonModule } from 'primeng/button';
import { ToastModule } from 'primeng/toast';
import { InputTextModule } from 'primeng/inputtext';
import { ProgressBarModule } from 'primeng/progressbar';
import { DropdownModule } from 'primeng/dropdown';
import { MatSortModule } from '@angular/material/sort';
import { MatPaginatorModule } from '@angular/material/paginator';
import { AudiencesComponent } from './audiences/audiences.component';
import { MenuModule } from 'primeng/menu';
import { RippleModule } from 'primeng/ripple';
import { MenubarModule } from 'primeng/menubar';
import { SafePipe } from './services/safe.pipe';
import { ConsumerInsightsComponent } from './consumer-insights/consumer-insights.component';
import { TrendspottingComponent } from './trendspotting/trendspotting.component';
import { MatNativeDateModule } from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { DatePipe } from '@angular/common';
import { EmailCopyComponent } from './email-copy/email-copy.component';
import { SocialMediaPostComponent } from './social-media-post/social-media-post.component';
import { CarouselModule } from 'primeng/carousel';
import { NgxEditorModule } from 'ngx-editor';
import { NgxSimpleTextEditorModule } from 'ngx-simple-text-editor';
import { EditImageCanvasComponent } from './edit-image-canvas/edit-image-canvas.component';
import { WebsitePostComponent } from './website-post/website-post.component';
import { WebsitePostEditImageComponent } from './website-post-edit-image/website-post-edit-image.component';
import { SocialMediaEditCanvasComponent } from './social-media-edit-canvas/social-media-edit-canvas.component';
import { AssetGroupPmaxComponent } from './asset-group-pmax/asset-group-pmax.component';
import { ContentReviewComponent } from './content-review/content-review.component';
import { UserPhotoComponent } from './user-photo/user-photo.component';
import { Auth, getAuth, provideAuth } from '@angular/fire/auth';
import { environment } from '../environments/environments';
import { SortAmountDownIcon } from 'primeng/icons/sortamountdown';
import { SortAltIcon } from 'primeng/icons/sortalt';
import { SortAmountUpAltIcon } from 'primeng/icons/sortamountupalt';
import { ClipboardModule } from '@angular/cdk/clipboard';
import { PrismComponent } from './prism/prism.component';
import 'prismjs/components/prism-sql';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatSelectModule } from '@angular/material/select';

const fireBaseConfig = environment.firebaseConfig
@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    CampaignFormComponent,
    LoginComponent,
    LoginButtonComponent,
    UserJourneyComponent,
    ToggelButtonsComponent,
    ArchitectureDiagramComponent,
    CampaignListComponent,
    MarketingInsightsComponent,
    CampaignPerformanceComponent,
    ExistingCampaignsComponent,
    AudiencesComponent,
    SafePipe,
    ConsumerInsightsComponent,
    TrendspottingComponent,
    EmailCopyComponent,
    SocialMediaPostComponent,
    EditImageCanvasComponent,
    WebsitePostComponent,
    WebsitePostEditImageComponent,
    SocialMediaEditCanvasComponent,
    AssetGroupPmaxComponent,
    ContentReviewComponent,
    UserPhotoComponent,
    PrismComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    DialogModule,
    MatSlideToggleModule,
    HttpClientModule,
    MaterialModule,
    NgxDocViewerModule,
    FormsModule,
    TableModule,
    CalendarModule,
    SliderModule,
    DialogModule,
    MultiSelectModule,
    ContextMenuModule,
    DropdownModule,
    ButtonModule,
    ToastModule,
    InputTextModule,
    ProgressBarModule,
    MatSortModule,
    MenuModule,
    RippleModule,
    MenubarModule,
    MatPaginatorModule,
    MatFormFieldModule,
    MatInputModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatIconModule,
    CarouselModule,
    FormsModule,
    ReactiveFormsModule,
    NgxSimpleTextEditorModule,
    SortAmountDownIcon,
    SortAltIcon,
    SortAmountUpAltIcon,
    ClipboardModule,
    MatExpansionModule,
    MatSelectModule
    ],
  providers: [
    // provideClientHydration(),
    //   provideHttpClient()
    importProvidersFrom([
      provideFirebaseApp(() => initializeApp(fireBaseConfig)),
      provideFirestore(() => getFirestore()),
      provideAuth(() => getAuth()),
      ]),
    CustomerService,
    DatePipe
  ],
  bootstrap: [AppComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule { }
