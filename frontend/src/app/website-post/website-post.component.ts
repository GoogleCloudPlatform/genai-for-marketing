import { Component } from '@angular/core';
import { LoginService } from '../services/login.service';
import { CampaignService } from '../services/campaign.service';
import { Observable, Subscription, map, of, startWith } from 'rxjs';
import { AudiencesService } from '../services/audiences.service';
import { EmailCopyService } from '../services/email-copy.service';
import { DomSanitizer } from '@angular/platform-browser';
import { DialogConfirmComponent } from '../dialog-confirm/dialog-confirm.component';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { BOLD_BUTTON, CUSTOM, EditorConfig, FONT_SIZE_SELECT, FORE_COLOR, IMAGE_INPUT, INDENT_BUTTON, ITALIC_BUTTON, JUSTIFY_CENTER_BUTTON, JUSTIFY_FULL_BUTTON, JUSTIFY_LEFT_BUTTON, JUSTIFY_RIGHT_BUTTON, LINK_INPUT, ORDERED_LIST_BUTTON, OUTDENT_BUTTON, SEPARATOR, STRIKE_THROUGH_BUTTON, ST_BUTTONS, SUBSCRIPT_BUTTON, SUPERSCRIPT_BUTTON, UNDERLINE_BUTTON, UNDO_BUTTON, UNLINK_BUTTON, UNORDERED_LIST_BUTTON } from 'ngx-simple-text-editor';
import { WebsitePostService } from '../services/website-post.service';
import { FormControl } from '@angular/forms';
export interface EmailCopy {
  images_base64_string?: any;
}
export interface CampaignNames {
  name: string;
}

export interface TranslationLanguage {
  language_code: string;
  language_name: string;
}
@Component({
  selector: 'app-website-post',
  templateUrl: './website-post.component.html',
  styleUrl: './website-post.component.scss'
})
export class WebsitePostComponent {
  showchatboot: boolean = false;
  userLoggedIn: boolean = false;
  photoURL: string | undefined;
  subscription: Subscription | undefined;
  userId: any;
  CampaignResults: any;
  CAMPAIGN_DATA: CampaignNames[] = []
  CAMPAIGN_DATA1: any[] = [];
  languageControl!: FormControl<TranslationLanguage | null | undefined>;
  filteredOptions!: Observable<TranslationLanguage[]>;
  selectedLang: any = '';
  langCodes = [
    { 'language_code': 'da-DK', 'language_name': 'da-DK-Neural2-D' },
    { 'language_code': 'en-AU', 'language_name': 'en-AU-Neural2-D' },
    { 'language_code': 'en-IN', 'language_name': 'en-IN-Neural2-A' },
    { 'language_code': 'en-IN', 'language_name': 'en-IN-Neural2-B' },
    { 'language_code': 'en-IN', 'language_name': 'en-IN-Neural2-C' },
    { 'language_code': 'en-IN', 'language_name': 'en-IN-Neural2-D' },
    { 'language_code': 'en-GB', 'language_name': 'en-GB-Neural2-A' },
    { 'language_code': 'en-GB', 'language_name': 'en-GB-Neural2-B' },
    { 'language_code': 'en-GB', 'language_name': 'en-GB-Neural2-C' },
    { 'language_code': 'en-GB', 'language_name': 'en-GB-Neural2-D' },
    { 'language_code': 'en-GB', 'language_name': 'en-GB-Neural2-F' },

    { 'language_code': 'fil-PH', 'language_name': 'fil-ph-Neural2-A' },
    { 'language_code': 'fil-PH', 'language_name': 'fil-ph-Neural2-D' },
    { 'language_code': 'fr-CA', 'language_name': 'fr-CA-Neural2-A' },
    { 'language_code': 'fr-CA', 'language_name': 'fr-CA-Neural2-B' },
    { 'language_code': 'fr-CA', 'language_name': 'fr-CA-Neural2-C' },
    { 'language_code': 'fr-CA', 'language_name': 'fr-CA-Neural2-D' },
    { 'language_code': 'fr-FR', 'language_name': 'fr-FR-Neural2-A' },
    { 'language_code': 'fr-FR', 'language_name': 'fr-FR-Neural2-B' },
    { 'language_code': 'fr-FR', 'language_name': 'fr-FR-Neural2-C' },
    { 'language_code': 'fr-FR', 'language_name': 'fr-FR-Neural2-D' },
    { 'language_code': 'fr-FR', 'language_name': 'fr-FR-Neural2-E' },
    { 'language_code': 'fr-FR', 'language_name': 'fr-FR-Polyglot-1' },

    { 'language_code': 'de-DE', 'language_name': 'de-DE-Neural2-A' },
    { 'language_code': 'de-DE', 'language_name': 'de-DE-Neural2-B' },
    { 'language_code': 'de-DE', 'language_name': 'de-DE-Neural2-C' },
    { 'language_code': 'de-DE', 'language_name': 'de-DE-Neural2-D' },
    { 'language_code': 'de-DE', 'language_name': 'de-DE-Neural2-F' },
    { 'language_code': 'de-DE', 'language_name': 'de-DE-Polyglot-1' },

    { 'language_code': 'hi-IN', 'language_name': 'hi-IN-Neural2-A' },
    { 'language_code': 'hi-IN', 'language_name': 'hi-IN-Neural2-B' },
    { 'language_code': 'hi-IN', 'language_name': 'hi-IN-Neural2-C' },
    { 'language_code': 'hi-IN', 'language_name': 'hi-IN-Neural2-D' },

    { 'language_code': 'it-IT', 'language_name': 'it-IT-Neural2-A' },
    { 'language_code': 'it-IT', 'language_name': 'it-IT-Neural2-C' },

    { 'language_code': 'ja-JP', 'language_name': 'ja-JP-Neural2-B' },
    { 'language_code': 'ja-JP', 'language_name': 'ja-JP-Neural2-C' },
    { 'language_code': 'ja-JP', 'language_name': 'ja-JP-Neural2-D' }


  ]
  filtered!: any;
  id: any;
  campaignData: any;
  audiences: any;
  showCampaignDropdown: boolean = false
  showAudienceMessage: boolean = false
  audiencesEmailsandtrasctionData: any;
  showCampaignData: boolean = false;
  val: string = '';
  imageData: any | undefined;
  emailCopy!: any;
  images: any[] = [];
  textContent: string | undefined;
  image_base64: string | undefined;
  showProgress: boolean = false;
  fileUploaded: boolean = false;
  uploadImageAssetsClicked: boolean = false;
  generateImageClicked: boolean = false;
  showGenerateImagedata: boolean = false;
  showImageGenarateBtn: boolean = false;
  public files: any[] = [];
  showUploadImageData: boolean = false;
  saveCampaignId: any;
  imageSrc: any;
  editImageSection: boolean = false;
  showEmailContents: boolean = false;
  colorTone: any = 'Cool tone';
  lighting: any = 'Golden hour';
  compostion: any = 'Wide angle';
  aspectsRatio: any = '1:1';
  ContentType: any = 'Photo';
  config: EditorConfig = {
    placeholder: 'Type something...',
    buttons: [UNDO_BUTTON, SEPARATOR, BOLD_BUTTON, ITALIC_BUTTON, UNDERLINE_BUTTON, STRIKE_THROUGH_BUTTON, JUSTIFY_LEFT_BUTTON, JUSTIFY_CENTER_BUTTON,
      JUSTIFY_RIGHT_BUTTON, JUSTIFY_FULL_BUTTON, ORDERED_LIST_BUTTON, UNORDERED_LIST_BUTTON, INDENT_BUTTON,
      OUTDENT_BUTTON, FONT_SIZE_SELECT,
      LINK_INPUT, UNLINK_BUTTON, FORE_COLOR]
  };
  edit_mask_tools: CampaignNames[] = [{ name: "Rectangle" }, { name: "Brush" }, { name: "Circle" }, { name: "Move/Scale/Rotate" }]
  showSaveSpinner: boolean = false;
  campaignId: any;
  selectedCampaignFromDropdown: any;
  selectedImage: any
  showGenarateImageEmaildata: boolean = false;
  showEmailCopySave: boolean = false;
  showImagesUploaded: boolean = false;
  selectButtonId: any;
  campaignName: any;
  showSaveBtn: boolean = false;
  selectDisable: boolean = false;
  audio_url: any;
  constructor(public loginService: LoginService, public audiencesSerive: AudiencesService,
    public websitePostService: WebsitePostService, private domSanitizer: DomSanitizer, private snackBar: MatSnackBar,
    public campaignServ: CampaignService, public dialog: MatDialog, private _snackBar: MatSnackBar,) {

    this.subscription = this.loginService.getUserDetails().subscribe(res => {
      this.userLoggedIn = true;
      this.photoURL = res?.photoURL;
      this.userId = res?.uid
    });
  }
  ngOnInit() {
    this.getCampaign();
    this.languageControl = new FormControl<TranslationLanguage | null | undefined>(this.langCodes.find(i => i.language_code === 'en-IN'));
    this.filteredOptions = of(this.langCodes)
  }

  private _filter(name: string): TranslationLanguage[] {
    const filterValue = name.toLowerCase();
    return this.langCodes.filter(option => option.language_name.toLowerCase().includes(filterValue));
  }

  onClickMarketingAssi() {
    this.showchatboot = true
  }

  getCampaign() {
    this.campaignServ.getCampaigns(this.userId).subscribe((res: any) => {
      this.CampaignResults = res.results;
      if (this.CampaignResults.length > 0) {
        this.showCampaignDropdown = true;
      } else {
        this.showCampaignDropdown = false;
      }
      this.CAMPAIGN_DATA1 = res.results;
      this.CAMPAIGN_DATA = this.CampaignResults?.map((res: any) => {
        return { name: res.data.name, id: res.id };
      })
      this.campaignId = this.CampaignResults[0].id;
    });
  }

  onClickCampaign(selectedValue: any) {
    this.campaignName = selectedValue;
    this.clearExistingData();
    this.onGenerateImage();
    this.filtered = this.CAMPAIGN_DATA1.filter(a => a.data.name === selectedValue)
    this.filtered.forEach((element: { data: any; id: any }) => {
      this.id = element.id;
      this.campaignData = element.data;
      this.audiences = element.data.audiences
      this.showCampaignData = true
      this.selectedCampaignFromDropdown = this.CampaignResults.filter((c: any) => c.id === this.id);
      this.val = this.selectedCampaignFromDropdown[0]?.data?.theme
    });
  }

  onGenerateImage() {
    this.generateImageClicked = true
    this.showGenerateImagedata = true
    this.uploadImageAssetsClicked = false
    this.showUploadImageData = false;
    this.showEmailCopySave = true;
    this.showGenarateImageEmaildata = false;
    this.clearExistingData();
    this.fileUploaded = false;
    this.editImageSection = false;
    this.selectedImage = '';
    this.images = []
  }
  onUploadImageAssets() {
    this.uploadImageAssetsClicked = true
    this.showUploadImageData = true;
    this.generateImageClicked = false
    this.showGenerateImagedata = false
    this.showEmailContents = false
    this.showGenarateImageEmaildata = true;
    this.showEmailCopySave = false;
    this.textContent = "";
    this.images = [];
    this.fileUploaded = false;
    this.clearExistingGenImageData();
    this.selectedImage = ''
  }

  clearExistingGenImageData() {
    this.editImageSection = false;

  }
  onClickAspectRation(selectedValue: any) {
    this.aspectsRatio = selectedValue
  }

  onClickContentType(selectedValue: any) {
    this.ContentType = selectedValue
  }

  onClickColorTone(selectedValue: any) {
    this.colorTone = selectedValue
  }
  onClickLighting(selectedValue: any) {
    this.lighting = selectedValue
  }
  onClickCompostion(selectedValue: any) {
    this.compostion = selectedValue
  }

  generateEmailTextWebsitePost() {

    if (this.showGenarateImageEmaildata) {
      this.showProgress = true
      let obj = {
        "type": "Webpost",
        "theme": this.selectedCampaignFromDropdown[0].data.theme,
        "context": this.val,
        "no_of_char": 500,
        "audience_age_range": this.selectedCampaignFromDropdown[0].data.brief.age_select_theme,
        "audience_gender": this.selectedCampaignFromDropdown[0].data.brief.gender_select_theme,
        "image_generate": false,
        "prompt": "theme:" + this.selectedCampaignFromDropdown[0].data.name
      }
      this.websitePostService.generateEmailTextWebsitePost(obj).subscribe((res: any) => {
        this.textContent = res.generated_content.text;
        this.showEmailContents = true;
        this.showProgress = false;
      });
    }
    else {
      if (this.val === "") {
        alert('please enter context value')

      }
      else {
        this.showProgress = true
        let obj = {
          "type": "Webpost",
          "theme": this.selectedCampaignFromDropdown[0].data?.theme,
          "context": this.val,
          "no_of_char": 500,
          "audience_age_range": this.selectedCampaignFromDropdown[0].data.brief.age_select_theme,
          "audience_gender": this.selectedCampaignFromDropdown[0].data.brief.gender_select_theme,
          "image_generate": false,
          "prompt": "theme:" + this.val + ",aspect_ration: " + this.aspectsRatio + ",color_tone:" + this.colorTone
            + ", lighting:" + this.lighting + ",compostion:" + this.compostion + ",content_type:" + this.ContentType
        }
        this.websitePostService.generateEmailTextWebsitePost(obj).subscribe((res: any) => {
          this.textContent = res.generated_content.text;
          this.showEmailContents = true;
          this.generateImageWebsitePost()
        });
      }
    }
    // this.showProgress = false
  }

  generateImageWebsitePost() {
    let obj = {
      "prompt": "Theme:" + this.selectedCampaignFromDropdown[0].data.theme + " " + this.val + ", Aspect Ration: " + this.aspectsRatio + ", Color Tone:" + this.colorTone
        + ", Lighting:" + this.lighting + ", Composition:" + this.compostion + ", Content Type:" + this.ContentType,
      "number_of_images": 3,
      "negative_prompt": ""
    }

    //this.showImageGenarateBtn = false
    this.websitePostService.generateImageWebsitePost(obj).subscribe((res: any) => {

      this.images = []
      res.generated_images.forEach((element: { images_base64_string: string; id: any }) => {
        this.emailCopy = this.domSanitizer.bypassSecurityTrustResourceUrl('data:image/jpg;base64,'
          + element.images_base64_string);
        this.images.push({ id: element.id, image: this.emailCopy });
        this.showProgress = false;
        this.showImageGenarateBtn = true
      });
    });
  }

  loadEditImageCanvasComponent(img: any) {
    this.editImageSection = true;
    //this.imageSrc = img.changingThisBreaksApplicationSecurity
    this.imageSrc = img.changingThisBreaksApplicationSecurity || img;
  }

  updateCanvasImage(base64String: any) {
    this.selectedImage = base64String;
    this.showEmailCopySave = true;
  }

  saveImageToDrive() {
    this.showSaveSpinner = true;
    if (this.selectedImage?.changingThisBreaksApplicationSecurity) {
      this.selectedImage = this.selectedImage?.changingThisBreaksApplicationSecurity
    }
    if (!this.selectedImage) {
      this.selectedImage = this.images[0].image;
    }
    var selectedImage = this.campaignServ.dataURLtoFile(`${this.selectedImage}`, 'website_post_image.png')
    let selectedCampaign = this.CampaignResults.filter((c: any) => c.id === this.campaignId);
    let folder_id = selectedCampaign[0].data.workspace_assets.new_folder_id
    this.campaignServ.imageUploadToGCS(selectedImage, folder_id, event).subscribe((res: any) => {
      this.saveCampaignId = res;
      this.saveCampaignWebsitePost(this.saveCampaignId, selectedCampaign)
    })
  }

  saveCampaignWebsitePost(saveCampaignId: any, selectedCampaign: any) {
    this.showSaveSpinner = true;
    let websitePost = {
      'text': this.textContent,
      'gcs_path': saveCampaignId
    }
    selectedCampaign[0].data.website_post = websitePost
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
      // "campaign_uploaded_images": { saveCampaignId },
      "status": selectedCampaign[0].data.status
    }
    this.websitePostService.updateCampaignWebsitePost(obj, this.userId, this.campaignId).subscribe((res: any) => {
      this.showSnackbar(res?.message, 'Close', '4000');
      this.showSaveSpinner = false
    });
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

  onClickSelect(image: any, id: any) {
    this.selectedImage = image.changingThisBreaksApplicationSecurity;
    this.selectButtonId = id;
    this.selectDisable = true;
    this.showSaveBtn = true;
  }

  onFileChange(pFileList: File[]) {
    this.showProgress = true;
    let selectedCampaign: any
    selectedCampaign = this.CAMPAIGN_DATA1.filter((a: any) => a.id === this.id)
    this.fileUploaded = true;
    const reader = new FileReader();

    this.campaignServ.imageUpload(pFileList[0], selectedCampaign[0].data?.workspace_assets?.new_folder_id, event).subscribe((res: any) => {
      reader.addEventListener('load', (event: any) => {
        this.imageSrc = event.target.result;
        this.images.push({ id: 1, image: this.imageSrc });
        this.showImagesUploaded = true;
      });
      reader.readAsDataURL(pFileList[0]);
      this.saveCampaignId = res;
      this.files = Object.keys(pFileList).map((key: any) => pFileList[key]);
      this.showProgress = false;
      this.showGenarateImageEmaildata = true;
      this._snackBar.open("Successfully upload!", 'Close', {
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

  clearExistingData() {
    //clear all data here on campaign change
    this.uploadImageAssetsClicked = false;
    this.showUploadImageData = false;
    this.files = [];
    this.editImageSection = false;
    this.showEmailContents = false;
    this.textContent = "";
    this.val = "";
    this.showImagesUploaded = false;
    this.images = [];
    this.imageSrc = "";
  }


  updateEmailText(value: any) {
    this.textContent = value;
  }

  showSaveButton(val: boolean) {
    this.showSaveBtn = val
  }

  changeLang(event: any) {
    this.audio_url = "";
    let selectedCampaign = this.CampaignResults.filter((c: any) => c.id === this.campaignId);
    let folder_id = selectedCampaign[0].data.workspace_assets.new_folder_id
    let today = new Date();
    this.languageControl.patchValue(event);
    let obj = {
      "text": this.textContent,
      "prefix": `${folder_id}/webpost_audio_${today.toISOString()}`,
      "language_code": event.language_code,
      "language_name": event.language_name
    }
    this.websitePostService.generateTextToSpeech(obj).subscribe((res: any) => {
      let str = res.audio_uri
      let newstr = str.replace("gs://", "https://storage.googleapis.com/");
      console.log(newstr)
      this.audio_url = newstr
    })
  }
}
