import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AudiencesService } from '../services/audiences.service';
import { CampaignService } from '../services/campaign.service';
import { LoginService } from '../services/login.service';
import { EmailCopyService } from '../services/email-copy.service';
import { FormControl, FormGroup } from '@angular/forms';
import { SocialMediaService } from '../services/social-media.service';
import { DomSanitizer } from '@angular/platform-browser';
export interface CampaignNames {
  name: string;
}
@Component({
  selector: 'app-social-media-post',
  templateUrl: './social-media-post.component.html',
  styleUrl: './social-media-post.component.scss'
})

export class SocialMediaPostComponent {
  showchatboot: boolean = false;
  userLoggedIn: boolean = false;
  photoURL: string | undefined;
  userId: any;
  campaignResults: any;
  CAMPAIGN_DATA: CampaignNames[] = []
  CAMPAIGN_DATA1: any[] = [];
  filtered!: any;
  selectedCampaignId: any;
  campaignData: any;
  audiences: any;
  showCampaignDropdown: boolean = false
  showAudienceMessage: boolean = false
  audiencesEmailsandtrasctionData: any;
  showGenerateImageAsset: boolean = false;
  showCampaignData: boolean = false;
  promptVal: string = '';
  imageData: any | undefined;
  imageRes!: any;
  images: any[] = [];
  textContent: string | undefined;
  image_base64: string | undefined;
  showProgress: boolean = false;
  fileUploaded: boolean = false;
  sanitizedOutput: any = {};
  uploadImageAssetsClicked: boolean = false;
  genrateImageClicked: boolean = false;
  showGenarateImagedata: boolean = false;
  showImageGenarateBtn: boolean = false;
  selectButtonClick: boolean = false;
  public files: any[] = [];
  showUploadImageData: boolean = false;
  imageGcsPath: any;
  imageSrc: any;
  editImageSection: boolean = false;
  showEmailContents: boolean = false;
  showProgressLoader: boolean = false
  content = '';
  editEmailCont: any
  selectedCampaignFromDropdown: any;
  selectedImage: any;
  showImageSection: boolean = false;
  socialMediaForm = new FormGroup({
    aspectRation: new FormControl("1:1"),
    contentType: new FormControl("Photo"),
    colorTone: new FormControl("Cool tone"),
    lighting: new FormControl("Golden hour"),
    compostion: new FormControl("Wide angle"),
  });
  showEmailCopySave: boolean = false;
  hashtagValue: any;
  selectedDestination: any = "Instagram";
  showImagesUploaded: boolean = false;
  showGenarateImageEmaildata: boolean = false;
  showGenerateImageData: boolean = false;
  showGenerateButtonForUpload: boolean = false;
  showPostSection: boolean = false;
  selectButtonId: any;
  campaignName: any;
  saveSpinner: boolean = false;
  showSaveBtn: boolean = false;
  selectDisable: boolean = false;
  constructor(public loginService: LoginService, public audiencesSerive: AudiencesService, public snackBar: MatSnackBar,
    public emailService: EmailCopyService,
    public campaignServ: CampaignService, public socialmediaService: SocialMediaService, private domSanitizer: DomSanitizer) {
    this.loginService.getUserDetails().subscribe(res => {
      this.userLoggedIn = true;
      this.photoURL = res?.photoURL;
      this.userId = res?.uid
    });
  }
  ngOnInit() {
    this.getCampaign();
    this.showGenerateImageAsset = true;
    this.showGenerateImageData = true;
    this.genrateImageClicked = true;
  }
  onClickMarketingAssi() {
    this.showchatboot = true
  }
  onGenarteImage() {
    this.genrateImageClicked = true;
    this.uploadImageAssetsClicked = false;
    this.fileUploaded = false;
    this.showGenerateButtonForUpload = false;
    this.textContent = "";
    this.hashtagValue = ""
    this.images = [];
    this.fileUploaded = false;
    this.showGenerateImageData = true;
    this.showGenerateButtonForUpload = false;
    this.showPostSection = false;
    this.showUploadImageData = false;
    this.editImageSection = false;
    this.showImageSection = false;
    this.selectedImage =''
  }
  onUploadImageAssets() {
    this.genrateImageClicked = false;
    this.uploadImageAssetsClicked = true
    this.showUploadImageData = true;
    this.showGenarateImagedata = false
    this.showEmailContents = false
    this.textContent = "";
    this.hashtagValue = "";
    this.showPostSection = false;
    this.images = [];
    this.fileUploaded = false;
    this.showGenerateImageData = false;
    this.showGenerateButtonForUpload = true;
    this.showImageSection = false;
    this.editImageSection = false;
    this.imageSrc = '';
    this.selectedImage =''
  }
  loadEditImageCanvasComponent(img: any) {
    this.editImageSection = false;
    this.imageSrc = img.changingThisBreaksApplicationSecurity || img;
    this.editImageSection = true;
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
    });
  }

  onClickCampaign(selectedValue: any) {
    this.campaignName = selectedValue;
    this.filtered = this.CAMPAIGN_DATA1.filter(a => a.data.name === selectedValue)
    this.filtered.forEach((element: { data: any; id: any }) => {
      this.selectedCampaignId = element.id;
      this.campaignData = element.data;
      this.audiences = element.data.audiences
      this.selectedCampaignFromDropdown = this.campaignResults.filter((c: any) => c.id === this.selectedCampaignId);
      this.promptVal = this.selectedCampaignFromDropdown[0]?.data?.theme
    });
    if (this.audiences == null) {
      this.showAudienceMessage = true;
    } else {
      this.showAudienceMessage = false
    }
  }

  selectable: boolean = true;

  chipLists = [{ name: 'Instagram' }, { name: 'Threads' }];


  isSelectedChip(chipValue: any) {
    this.selectedDestination = chipValue
  }

  generateSocialMediaImage() {
    this.images =[];
    if (this.promptVal === "") {
      alert('please enter context value')
    } else {
      this.showProgress = true
      let obj = {
        "prompt": "Theme:" + this.selectedCampaignFromDropdown[0].data.theme + " " + this.promptVal 
        + ", Aspect Ration: " + this.socialMediaForm.controls.aspectRation.value 
        + ", Color Tone:" + this.socialMediaForm.controls.colorTone.value
        + ", Lighting:" + this.socialMediaForm.controls.lighting.value 
        + ", Composition:" + this.socialMediaForm.controls.compostion.value 
        + ", Content Type:" + this.socialMediaForm.controls.contentType.value,
        "number_of_images": 3,
        "negative_prompt": ""
      }
      this.socialmediaService.generateImage(obj).subscribe((res: any) => {
        res.generated_images.forEach((element: { images_base64_string: string; id: any }) => {
          this.imageRes = this.domSanitizer.bypassSecurityTrustResourceUrl('data:image/jpg;base64,'
            + element.images_base64_string);
          this.images.push({ id: element.id, image: this.imageRes });
          this.showImageSection = true;
          this.showProgress = false;
          this.showImageGenarateBtn = true;
          this.generateSocialMediaPosts()
        });
      });
    }
  }
  generateSocialMediaPosts() {
    this.showProgress = true
    let obj = {
      "type": "SocialMedia",
      "theme": this.selectedCampaignFromDropdown[0].data.theme,
      "context": this.promptVal,
      "no_of_char": 500,
      "audience_age_range": this.selectedCampaignFromDropdown[0].data.brief.age_select_theme,
      "audience_gender": this.selectedCampaignFromDropdown[0].data.brief.gender_select_theme,
      "image_generate": false,
      "prompt": "theme:" + this.selectedCampaignFromDropdown[0].data.theme
        + ",aspect_ration: " + this.socialMediaForm.controls.aspectRation.value
        + ",color_tone:" + this.socialMediaForm.controls.colorTone.value
        + ", lighting:" + this.socialMediaForm.controls.lighting.value
        + ",compostion:" + this.socialMediaForm.controls.compostion.value
        + ",content_type:" + this.socialMediaForm.controls.contentType.value
    }
    this.emailService.generateEmailText(obj).subscribe((res: any) => {

      let hashtags = res.generated_content.text.match(/#[a-z]+/gi);
      this.textContent = res.generated_content.text;
      this.hashtagValue = hashtags
      this.showEmailContents = true;
      this.showProgress = false;
      this.showImageSection = true;
      this.showPostSection = true;
    });
  }

  onClickSelect(image: any, id: any) {
    this.selectedImage = image.changingThisBreaksApplicationSecurity;
    this.selectButtonId = id;
    this.showSaveBtn = true;
    this.selectDisable = true;
  }
  updateCanvasImage(base64String: any) {
    this.selectedImage = base64String;
    this.showEmailCopySave = true;
    //this.showGenarateImagedata = true;
    // var cust=this.customers.find(e => e.customerNo==customer.customerNo)
    // Object.assign(cust,customer)
  }

  saveImageToDrive(){
    this.saveSpinner = true;
    if(this.selectedImage?.changingThisBreaksApplicationSecurity){
      this.selectedImage = this.selectedImage?.changingThisBreaksApplicationSecurity
    }
    if (!this.selectedImage) {
      this.selectedImage = this.images[0].image;
    }
    var selectedImage = this.campaignServ.dataURLtoFile(`${this.selectedImage}`, 'social_media_image.png')
    let selectedCampaign = this.campaignResults.filter((c: any) => c.id === this.selectedCampaignId);
    let folder_id  = selectedCampaign[0].data.workspace_assets.new_folder_id
    this.campaignServ.imageUploadToGCS(selectedImage, folder_id, event).subscribe((res: any) => {
      this.imageGcsPath = res;
      this.saveToCampaign(this.imageGcsPath , selectedCampaign)
    })
  }

  saveToCampaign(imageGcsPath : any ,  selectedCampaign : any) {
    this.saveSpinner = true;
    if (this.selectedDestination == "Instagram") {
      let instaData = {
        'text': this.textContent,
        'gcs_path': imageGcsPath
      }
      let obj = {
        "name": selectedCampaign[0].data.name,
        "theme": selectedCampaign[0].data.theme,
        "brief": selectedCampaign[0].data.brief,
        "emails": selectedCampaign[0].data.emails,
        "website_post": selectedCampaign[0].data.website_post,
        "ads_threads": selectedCampaign[0].data.ads_threads,
        "ads_insta": instaData,
        "asset_classes_text": selectedCampaign[0].data.asset_classes_text,
        "asset_classes_images": selectedCampaign[0].data.asset_classes_images,
        "workspace_assets": selectedCampaign[0].data.workspace_assets,
        "trendspotting_summaries": selectedCampaign[0].data.trendspotting_summaries,
        "audiences": selectedCampaign[0].data.audiences,
        "campaign_uploaded_images": selectedCampaign[0].campaign_uploaded_images,
        "status": selectedCampaign[0].data.status
      }

      this.audiencesSerive.updateCampaign(obj, this.userId, this.selectedCampaignId).subscribe((res: any) => {
        this.showSnackbar(res?.message, 'Close', '4000');
        this.saveSpinner = false;
      });
    }
    else {
      let threadData = {
        'text': this.textContent,
        'gcs_path': imageGcsPath
      }
      let obj = {
        "name": selectedCampaign[0].data.name,
        "theme": selectedCampaign[0].data.theme,
        "brief": selectedCampaign[0].data.brief,
        "emails": selectedCampaign[0].data.emails,
        "website_post": selectedCampaign[0].data.website_post,
        "ads_threads": threadData,
        "ads_insta": selectedCampaign[0].data.ads_insta,
        "asset_classes_text": selectedCampaign[0].data.asset_classes_text,
        "asset_classes_images": selectedCampaign[0].data.asset_classes_images,
        "workspace_assets": selectedCampaign[0].data.workspace_assets,
        "trendspotting_summaries": selectedCampaign[0].data.trendspotting_summaries,
        "audiences": selectedCampaign[0].data.audiences,
        "campaign_uploaded_images": selectedCampaign[0].campaign_uploaded_images,
        "status": selectedCampaign[0].data.status
      }
      this.audiencesSerive.updateCampaign(obj, this.userId, this.selectedCampaignId).subscribe((res: any) => {
        this.showSnackbar(res?.message, 'Close', '4000');
        this.saveSpinner = false;
      });
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

  onFileChange(pFileList: File[]) {
    this.showProgress = true;
    let selectedCampaign: any
    selectedCampaign = this.CAMPAIGN_DATA1.filter((a: any) => a.id === this.selectedCampaignId)
    this.fileUploaded = true;
    const reader = new FileReader();

    this.campaignServ.imageUpload(pFileList[0], selectedCampaign[0].data?.workspace_assets?.new_folder_id, event).subscribe((res: any) => {
      reader.addEventListener('load', (event: any) => {
        this.imageSrc = event.target.result;
        this.images.push({ id: 1, image: this.imageSrc });
        this.showImagesUploaded = true;
        this.showImageSection = true;
        this.showPostSection = false;
      });
      reader.readAsDataURL(pFileList[0]);

      this.imageGcsPath = res;
      // this.editImageSection = true;
      this.files = Object.keys(pFileList).map((key: any) => pFileList[key]);
      this.showProgress = false;

      //this.showGenarateImagedata = true;
      this.showGenarateImageEmaildata = true;
      this.snackBar.open("Successfully upload!", 'Close', {
        duration: 2000,
      });
    })

  }
  formatBytes(bytes: any, decimals = 2) {
    if (!+bytes) return '0 Bytes'

    const k = 1024
    const dm = decimals < 0 ? 0 : decimals
    const sizes = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
  }

  updateSocialMediaText(value: any) {
    this.textContent = value;
  }

  updateHashTagVal(value: any) {
    this.hashtagValue = value;
  }
  showSaveButton(val: boolean) {
    this.showSaveBtn = val
  }
}



