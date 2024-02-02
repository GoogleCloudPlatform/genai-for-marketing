import { Component } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AudiencesService } from '../services/audiences.service';
import { CampaignService } from '../services/campaign.service';
import { EmailCopyService } from '../services/email-copy.service';
import { LoginService } from '../services/login.service';
import { AssetGroupPmaxService } from '../services/asset-group-pmax.service';
import { DomSanitizer } from '@angular/platform-browser';
import { Subscription } from 'rxjs';
export interface CampaignNames {
  name: string;
}
@Component({
  selector: 'app-asset-group-pmax',
  templateUrl: './asset-group-pmax.component.html',
  styleUrl: './asset-group-pmax.component.scss'
})

export class AssetGroupPmaxComponent {
  showHeadline: boolean = false;
  assetGroupPmaxForm = new FormGroup({
    selectedTool: new FormControl(),
    promptMsg: new FormControl(),

  });
  headlineValue!: any;
  longHeadlineValue!: any;
  descriptionValue!: any;
  callToActionValue!: any;
  userLoggedIn: boolean = false;
  photoURL: string | undefined;
  userId: any;
  campaignResults: any;
  CAMPAIGN_DATA: CampaignNames[] = []
  CAMPAIGN_DATA1: any[] = [];
  filtered!: any;
  selectedCampaignId: any;
  campaignData: any;
  selectedCampaignFromDropdown: any;
  showCampaignDropdown: boolean = false;
  showProgress: boolean = false;
  showchatboot: boolean = false;
  showCampaineDropdown: boolean = false
  showAudienceMessage: boolean = false
  audiencesEmailsandtrasctionData: any;
  showTabledata: boolean = false;
  showCampaignData: boolean = false;
  val: string = '';
  imageData: any | undefined;
  emailCopy!: any;
  images: any[] = [];
  base64Images: any[] = [];
  textContent: string | undefined;
  image_base64: string | undefined;
  fileUploaded: boolean = false;
  sanitizedOutput: any = {};
  uploadImageAssetsClicked: boolean = false;
  genrateImageClicked: boolean = false;
  showGenarateImagedata: boolean = false;
  showImageGenarateBtn: boolean = false;
  selectButtonClick: boolean = false;
  public files: any[] = [];
  showUploadImageData: boolean = false;
  saveCampaignId: any;
  imageSrc: any;
  editImageSection: boolean = false;
  showEmailContents: boolean = false;
  showProgressLoader: boolean = false
  content = '';
  colorTone: any;
  lighting: any;
  compostion: any;
  aspectsRatio: any;
  ContentType: any;
  editEmailCont: any
  edit_mask_tools: CampaignNames[] = [{ name: "Rectangle" }, { name: "Brush" }, { name: "Circle" }, { name: "Move/Scale/Rotate" }]
  campaignId: any;
  dataSource: any;
  displayedColumns = ['index', 'email'];
  selectedImage: any
  showGenarateImageEmaildata: boolean = false;
  showEmailCopySave: boolean = false;
  showImagesUploaded: boolean = false;
  headlines: any;
  long_headlines: any;
  description: any;
  imagesData: any;
  callToAction: any;
  campaignName: any;
  subscription: Subscription | undefined;
  showSpinner: boolean = false;
  constructor(public loginService: LoginService, public audiencesSerive: AudiencesService, public snackBar: MatSnackBar,
    public assetGroupPmaxService: AssetGroupPmaxService, private domSanitizer: DomSanitizer,
    public campaignServ: CampaignService,) {
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

  getCampaign() {
    this.campaignServ.getCampaigns(this.userId).subscribe((res: any) => {
      this.campaignResults = res.results;
      if (this.campaignResults.length > 0) {
        this.showCampaignDropdown = true;
      } else {
        this.showCampaignDropdown = false;
      }
      this.CAMPAIGN_DATA1 = res.results;
      this.CAMPAIGN_DATA = this.campaignResults?.map((res: any) => {
        return { name: res.data.name, id: res.id };
      })
      this.campaignId = this.campaignResults[0].id;
    });

  }

  onClickCampaign(selectedValue: any) {
    this.campaignName = selectedValue;
    this.filtered = this.CAMPAIGN_DATA1.filter(a => a.data.name === selectedValue)
    this.filtered.forEach((element: { data: any; id: any }) => {
      this.selectedCampaignId = element.id;
      this.campaignData = element.data;
      this.campaignId = element.id
      this.selectedCampaignFromDropdown = this.campaignResults.filter((c: any) => c.id === this.selectedCampaignId);

    });
  }
  generateImage() {
    let obj = {
      "prompt": "theme:" + this.selectedCampaignFromDropdown[0].data.theme + ",aspect_ration: " + this.aspectsRatio + ",color_tone:" + this.colorTone
        + ", lighting:" + this.lighting + ",compostion:" + this.compostion + ",content_type:" + this.ContentType,
      "number_of_images": 3,
      "negative_prompt": ""
    }

    this.assetGroupPmaxService.generateImages(obj).subscribe((res: any) => {
      this.images = []
      this.base64Images = []
      this.imagesData = res.generated_images
      res.generated_images.forEach((element: { images_base64_string: string; }) => {
        this.emailCopy = this.domSanitizer.bypassSecurityTrustResourceUrl('data:image/jpg;base64,'
          + element.images_base64_string);
        this.images.push(this.emailCopy);
        this.showProgress = false;
        this.showImageGenarateBtn = true
      });

      res.generated_images.forEach((element: { images_base64_string: string; }) => {
        this.base64Images.push(element.images_base64_string);

      });
    });
  }

  generateTextContents() {
    if (this.showGenarateImageEmaildata) {
      this.showProgress = true
      let obj = {
        "type": "AssetGroup",
        "theme": this.selectedCampaignFromDropdown[0].data.name,
        "context": "",
        "no_of_char": 500,
        "audience_age_range": this.selectedCampaignFromDropdown[0].data.brief.age_select_theme,
        "audience_gender": this.selectedCampaignFromDropdown[0].data.brief.gender_select_theme,
        "image_generate": false,
        "prompt": "theme:" + this.selectedCampaignFromDropdown[0].data.name
      }
      this.assetGroupPmaxService.generateTextContents(obj).subscribe((res: any) => {
        this.textContent = res.generated_content;
        this.headlines = res.generated_content.headlines
        this.long_headlines = res.generated_content.long_headlines
        this.description = res.generated_content.description
        this.showEmailContents = true;
      });
    } else {
      this.showProgress = true
      let obj = {
        "type": "AssetGroup",
        "theme": this.selectedCampaignFromDropdown[0].data.name,
        "context": "",
        "no_of_char": 500,
        "audience_age_range": this.selectedCampaignFromDropdown[0].data.brief.age_select_theme,
        "audience_gender": this.selectedCampaignFromDropdown[0].data.brief.gender_select_theme,
        "image_generate": false,
        "prompt": "theme:" + this.val + ",aspect_ration: " + this.aspectsRatio + ",color_tone:" + this.colorTone
          + ", lighting:" + this.lighting + ",compostion:" + this.compostion + ",content_type:" + this.ContentType
      }
      this.assetGroupPmaxService.generateTextContents(obj).subscribe((res: any) => {
        this.textContent = res.generated_content;
        this.headlines = res.generated_content.headlines
        this.long_headlines = res.generated_content.long_headlines
        this.description = res.generated_content.description
        this.callToAction = res.generated_content.call_to_action
        this.showEmailContents = true;
        this.generateImage();
      });
    }
  }

  saveToCampaign(saveCampaignId: any , imageGcsPath : any) {
    let selectedCampaign = this.campaignResults.filter((c: any) => c.id === this.campaignId);
    selectedCampaign[0].data.asset_classes_text = this.textContent
    let obj = {
      "name": selectedCampaign[0].data.name,
      "theme": selectedCampaign[0].data.theme,
      "brief": selectedCampaign[0].data.brief,
      "emails": selectedCampaign[0].data.emails,
      "website_post": selectedCampaign[0].data.website_post,
      "ads_threads": selectedCampaign[0].data.ads_threads,
      "ads_insta": selectedCampaign[0].data.ads_insta,
      "asset_classes_text": selectedCampaign[0].data.asset_classes_text,
      "asset_classes_images": imageGcsPath,
      "workspace_assets": selectedCampaign[0].data.workspace_assets,
      "trendspotting_summaries": selectedCampaign[0].data.trendspotting_summaries,
      "audiences": selectedCampaign[0].data.audiences,
      "status": selectedCampaign[0].data.status,
     // "campaign_uploaded_images": { saveCampaignId }
    }
    this.assetGroupPmaxService.updateCampaignWebsitePost(obj, this.userId, this.campaignId).subscribe((res: any) => {
      // this.showSnackbar(res?.message, 'Close', '4000')
    });
  }

  async saveCampaign() {
    this.showSpinner = true;
    let imageGcsPath: any[] =[]
    let selectedCampaign = this.campaignResults.filter((c: any) => c.id === this.campaignId);
    let folder_id = selectedCampaign[0].data.workspace_assets.new_folder_id;
    let asset_group_image: any = ['asset_group_image_1', 'asset_group_image_2', 'asset_group_image_3']
    for (let i = 0; i < this.base64Images.length; i++) {
      const base64Response = await fetch(`data:image/jpeg;base64,${this.base64Images[i]}`);
      //asset_group_image[i] = await base64Response.blob();
      var file = this.campaignServ.dataURLtoFile(`data:image/jpeg;base64,${this.base64Images[i]}`, asset_group_image[i])
      this.campaignServ.imageUploadToGCS(file, folder_id, event).subscribe((res: any) => {
        this.saveCampaignId = res;
        imageGcsPath.push(res)
        this.saveToCampaign(this.saveCampaignId , imageGcsPath)
      })
      if (i == this.base64Images.length - 1) {
        this.showSnackbar("Successfully Updated", 'Close', '4000');
        this.showSpinner = false;
      }
    }
  }

  showSnackbar(content: any, action: any, duration: any) {
    let sb = this.snackBar.open(content, action, {
      duration: duration,
      panelClass: ["custom-style"]
    });
    sb.onAction().subscribe(() => {
      sb.dismiss();
    });
  }
}