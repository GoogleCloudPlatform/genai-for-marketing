import { Component } from '@angular/core';
import { LoginService } from '../services/login.service';
import { CampaignService } from '../services/campaign.service';
import { AsyncSubject, Observable, Subscription, forkJoin } from 'rxjs';
import { AudiencesService } from '../services/audiences.service';
import { EmailCopyService } from '../services/email-copy.service';
import { DomSanitizer } from '@angular/platform-browser';
import { DialogConfirmComponent } from '../dialog-confirm/dialog-confirm.component';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { BOLD_BUTTON, CUSTOM, EditorConfig, FONT_SIZE_SELECT, FORE_COLOR, IMAGE_INPUT, INDENT_BUTTON, ITALIC_BUTTON, JUSTIFY_CENTER_BUTTON, JUSTIFY_FULL_BUTTON, JUSTIFY_LEFT_BUTTON, JUSTIFY_RIGHT_BUTTON, LINK_INPUT, ORDERED_LIST_BUTTON, OUTDENT_BUTTON, SEPARATOR, STRIKE_THROUGH_BUTTON, ST_BUTTONS, SUBSCRIPT_BUTTON, SUPERSCRIPT_BUTTON, UNDERLINE_BUTTON, UNDO_BUTTON, UNLINK_BUTTON, UNORDERED_LIST_BUTTON } from 'ngx-simple-text-editor';
export interface EmailCopy {
  images_base64_string?: any;

}
export interface CampaignNames {
  name: string;
}
export interface SelectedFiles {
  name: string;
  file: any;
  base64?: string;
}
@Component({
  selector: 'app-email-copy',
  templateUrl: './email-copy.component.html',
  styleUrl: './email-copy.component.scss'
})
export class EmailCopyComponent {
  showchatboot: boolean = false;
  userLoggedIn: boolean = false;
  photoURL: string | undefined;
  subscription: Subscription | undefined;
  userId: any;
  CampaignResults: any;
  CAMPAIGN_DATA: CampaignNames[] = []
  CAMPAIGN_DATA1: any[] = [];
  filtered!: any;
  id: any;
  campaignData: any;
  audiences: any;
  showCampaignDropdown: boolean = false
  showAudienceMessage: boolean = false
  audiencesEmailsandtrasctionData: any;
  showTabledata: boolean = false;
  showCampaignData: boolean = false;
  contextVal: string = '';
  imageData: any | undefined;
  emailCopy!: any;
  images: any[] = [];
  textContent: string | undefined;
  image_base64: string | undefined;
  showProgress: boolean = false;
  showProgress2: boolean = false;
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
  colorTone: any = 'Cool tone';
  lighting: any = 'Golden hour';
  campostion: any = 'Wide angle';
  aspectsRatio: any = '1:1';
  ContentType: any = 'Photo';
  editEmailCont: any
  bulEmailfiltered!: any;
  bulEmailfiltered_DATA: any[] = [];
  bulEmailTextContent!: any;
  ShowBulkEmailContents: boolean = false;
  showButtonBulkEMail: boolean = false;
  bulEmailTextContentTranslate!: any;
  bulEmailTextContentEnglish!: any;
  activeEnglishButton: boolean = true
  activeETranslatedButton: boolean = false
  visibleEmails: any;
  startIndex: any = 0;
  activeEButton: boolean[] = [true, false, false];

  bulkEmailDisplay!: any;
  showSingleMailContent!: any;
  campaignName: any;
  config: EditorConfig = {
    placeholder: 'Type something...',
    buttons: [UNDO_BUTTON, BOLD_BUTTON, ITALIC_BUTTON,
      UNORDERED_LIST_BUTTON]
  };
  edit_mask_tools: CampaignNames[] = [{ name: "Rectangle" }, { name: "Brush" }, { name: "Circle" }, { name: "Move/Scale/Rotate" }]

  campaignId: any;
  dataSource: any;
  displayedColumns = ['email', 'first_name', 'language', 'age_group', 'gender', 'city'];
  selectedCampaignFromDropdown: any;
  public selectedFiles: SelectedFiles[] = [];
  selectedImage: any
  showGenarateImageEmaildata: boolean = false;
  showEmailCopySave: boolean = false;
  showImagesUploaded: boolean = false;
  selectButtonId: any;
  bulEmails: any;
  selectedEmail: any;
  saveSpinner: boolean = false;
  bulkEmailImageContent: any;
  bulkEmailLanguage: any;
  selectedBulkEmailIndex: number = 0;
  showSaveBtn: boolean = false;
  constructor(public loginService: LoginService, public audiencesSerive: AudiencesService,
    public emailService: EmailCopyService, private domSanitizer: DomSanitizer, private snackBar: MatSnackBar,
    public campaignServ: CampaignService, public dialog: MatDialog, private _snackBar: MatSnackBar,) {
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
    this.showchatboot = true;
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
      //on initial load set the 1st campaign details
      this.campaignId = this.CampaignResults[0].id;
      this.selectedCampaignFromDropdown = this.CampaignResults[0]
    });
  }

  onClickCampaign(selectedValue: any) {
    this.campaignName = selectedValue;
    this.clearExistingData()
    this.filtered = this.CAMPAIGN_DATA1.filter(a => a.data.name.trim() === selectedValue.trim())
    this.filtered.forEach((element: { data: any; id: any }) => {
      this.id = element.id;
      this.campaignData = element.data;
      this.audiences = element.data.audiences
      this.dataSource = element.data.audiences?.crm_data
      this.showCampaignData = true;
      this.selectedCampaignFromDropdown = this.CampaignResults.filter((c: any) => c.id === this.id);
      this.campaignId = element.id;
      this.contextVal = this.selectedCampaignFromDropdown[0]?.data?.theme
    });
    if (this.audiences == null) {
      this.showAudienceMessage = true;
    } else {
      this.showAudienceMessage = false;
      this.genrateImageClicked = true;
      this.showGenarateImagedata = true;
    }
    //this.getAudiencesEmailsandtrasctionData();
  }
  clearExistingData() {
    //clear all data here on campaign change
    this.uploadImageAssetsClicked = false;
    this.showUploadImageData = false;
    this.files = [];
    this.editImageSection = false;
    this.showEmailContents = false;
    this.textContent = "";
    this.contextVal = "";
    this.showImagesUploaded = false;
    this.images = [];
    this.imageSrc = "";
  }

  clearExistinggenImageData() {
    this.editImageSection = false;

  }
  getAudiencesEmailsandtrasctionData() {
    //this.showTabledata = true;
    this.showCampaignData = true
    this.audiencesSerive.getaudienceTableData().subscribe((res: any) => {
      this.audiencesEmailsandtrasctionData = res.audiences
    });
  }

  generateEmailCopy() {
    let obj = {
      "prompt": this.contextVal + ", Aspect Ration: " + this.aspectsRatio + ", Color Tone:" + this.colorTone
        + ", Lighting:" + this.lighting + ", Composition:" + this.campostion + ", Content Type:" + this.ContentType,
      "number_of_images": 3,
      "negative_prompt": ""
    }

    //this.showImageGenarateBtn = false
    this.emailService.generateEmailCopy(obj).subscribe((res: any) => {
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

  generateEmailText() {
    if (this.showGenarateImageEmaildata) {
      this.showProgress = true
      let obj = {
        "type": "Email",
        "theme": this.selectedCampaignFromDropdown[0].data.theme,
        "context": "Audience Age Range:" + this.selectedCampaignFromDropdown[0].data.brief.age_select_theme + ", Gender:"
          + this.selectedCampaignFromDropdown[0].data.brief.gender_select_theme,
        "no_of_char": 500,
        "audience_age_range": this.selectedCampaignFromDropdown[0].data.brief.age_select_theme,
        "audience_gender": this.selectedCampaignFromDropdown[0].data.brief.gender_select_theme,
        "image_generate": false
      }
      this.emailService.generateEmailText(obj).subscribe((res: any) => {
        this.textContent = res.generated_content.text;
        this.showEmailContents = true;
        this.showProgress = false;
      });
    } else {
      if (this.contextVal === "") {
        alert('please enter context value')

      } else {
        this.showProgress = true
        let obj = {
          "type": "Email",
          "theme": this.selectedCampaignFromDropdown[0].data.theme,
          "context": "Audience Age Range:" + this.selectedCampaignFromDropdown[0].data.brief.age_select_theme + ", Gender:"
            + this.selectedCampaignFromDropdown[0].data.brief.gender_select_theme,
          "no_of_char": 500,
          "audience_age_range": this.selectedCampaignFromDropdown[0].data.brief.age_select_theme,
          "audience_gender": this.selectedCampaignFromDropdown[0].data.brief.gender_select_theme,
          "image_generate": false
        }
        this.emailService.generateEmailText(obj).subscribe((res: any) => {
          this.textContent = res.generated_content.text;
          this.showEmailContents = true;
          //this.bulkEmail();
          this.generateEmailCopy();
        });
      }
    }
  }
  onGenerateImage() {
    this.genrateImageClicked = true
    this.showGenarateImagedata = true;
    this.uploadImageAssetsClicked = false;
    this.showGenarateImageEmaildata = false;
    this.showUploadImageData = false;
    this.showEmailCopySave = true;
    this.clearExistingData();
    this.fileUploaded = false;
    this.bulEmails = '';
    this.visibleEmails = '';
  }
  onUploadImageAssets() {
    this.uploadImageAssetsClicked = true
    this.showUploadImageData = true;
    // this.showTabledata = false
    this.genrateImageClicked = false
    this.showGenarateImagedata = false
    this.showEmailContents = false
    this.showGenarateImageEmaildata = true;
    this.showEmailCopySave = false;
    this.textContent = "";
    this.images = [];
    this.fileUploaded = false;
    this.showImagesUploaded = false;
    this.editImageSection = false;
    this.imageSrc = '';
    this.clearExistinggenImageData();
    this.bulEmails = '';
    this.visibleEmails = '';
    this.selectedImage = ''
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
        this.bulkEmailImageContent = this.images[0].image;
        this.showImagesUploaded = true;
        this.loadEditImageCanvasComponent(this.images[0].image)
      });
      reader.readAsDataURL(pFileList[0]);

      this.saveCampaignId = res;
      // this.editImageSection = true;
      this.files = Object.keys(pFileList).map((key: any) => pFileList[key]);
      this.showProgress = false;

      //this.showGenarateImagedata = true;
      this.showGenarateImageEmaildata = true;
      this._snackBar.open("Successfully upload!", 'Close', {
        duration: 2000,
      });
    })
  }
  saveUploadImageToGCS() {
    this.saveSpinner = true;
    this.selectedImage = this.selectedImage?.changingThisBreaksApplicationSecurity
    if (!this.selectedImage) {
      this.selectedImage = this.images[0].image;
    }
    let gcs_path = ''
    var selectedImage = this.campaignServ.dataURLtoFile(`${this.selectedImage}`, 'email_copy_upload_image.png')
    let selectedCampaign = this.CampaignResults.filter((c: any) => c.id === this.campaignId);
    let folder_id = selectedCampaign[0].data.workspace_assets.new_folder_id
    this.campaignServ.imageUploadToGCS(selectedImage, folder_id, event).subscribe((res: any) => {
      if (this.bulEmails.length > 0) {
        for (let i = 0; i < this.bulEmails.length; i++) {
          this.bulEmails[i].gcs_path = res;
        }
      } else {
        gcs_path = res;
      }
      let emailsData = {
        'text': this.textContent,
        'persionalized_emails': this.bulEmails,
        'gcs_path': gcs_path
      }
      this.saveToCampaign(emailsData, selectedCampaign)
    })
  }

  async uploadAllImagesAndSaveCampaign(folder_id: any, updatedBulkEmails: any, selectedCampaign: any) {
    let responses: any[] = [];
    let selectedImage: File;
    Promise.all(
      updatedBulkEmails.map((email: any, i: any) => {
        let base64ImageUrl = updatedBulkEmails[i].generated_image
        base64ImageUrl = this.domSanitizer.bypassSecurityTrustResourceUrl('data:image/jpg;base64,'
          + updatedBulkEmails[i].generated_image);

        selectedImage = this.campaignServ.dataURLtoFile(base64ImageUrl.changingThisBreaksApplicationSecurity, 'email_copy_generate_image_' + i)

        return new Promise((resolve: any) => {
          this.campaignServ.imageUploadToGCS(selectedImage, folder_id, event).subscribe((res: any) => {
            return new Promise(() => {
              this.saveCampaignId = res;
              updatedBulkEmails[i].gcs_path = res;
              responses[i] = updatedBulkEmails[i];
              resolve();
            });
          })
        });
      })
    ).then(() => {
      let keys = ['generated_image'];
      responses.forEach((x: any) => {
        keys.forEach(k => delete x[k])
      })
      let emailsData = {
        'text': this.textContent,
        'persionalized_emails': responses
      }
      this.saveToCampaign(emailsData, selectedCampaign)
    });
  }

  async saveGenerateImageToGCS() {
    this.saveSpinner = true;
    let selectedCampaign = this.CampaignResults.filter((c: any) => c.id === this.campaignId);
    let folder_id = selectedCampaign[0].data.workspace_assets.new_folder_id
    let updatedBulkEmails = this.bulEmails;

    this.uploadAllImagesAndSaveCampaign(folder_id, updatedBulkEmails, selectedCampaign);
  }
  saveToCampaign(emailsData: any, selectedCampaign: any) {
    selectedCampaign[0].data.emails = emailsData
    let obj = {
      "name": selectedCampaign[0].data.name,
      "theme": selectedCampaign[0].data.theme,
      "brief": selectedCampaign[0].data.brief,
      "emails": emailsData,
      "website_post": selectedCampaign[0].data.website_post,
      "ads_threads": selectedCampaign[0].data.ads_threads,
      "ads_insta": selectedCampaign[0].data.ads_insta,
      "asset_classes_text": selectedCampaign[0].data.asset_classes_text,
      "asset_classes_images": selectedCampaign[0].data.asset_classes_images,
      "workspace_assets": selectedCampaign[0].data.workspace_assets,
      "trendspotting_summaries": selectedCampaign[0].data.trendspotting_summaries,
      "audiences": selectedCampaign[0].data.audiences,
      "status": selectedCampaign[0].data.status
    }
    this.audiencesSerive.updateCampaign(obj, this.userId, this.campaignId).subscribe((res: any) => {
      this.showSnackbar(res?.message, 'Close', '4000')
      this.saveSpinner = false;
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
  deleteFile(f: any) {
    this.files = this.files.filter(function (w) { return w.name != f.name });
    this._snackBar.open("Successfully delete!", 'Close', {
      duration: 2000,
    });
  }

  openConfirmDialog(pIndex: any): void {
    const dialogRef = this.dialog.open(DialogConfirmComponent, {
      panelClass: 'modal-xs'
    });
    dialogRef.componentInstance.fName = this.files[pIndex].name;
    dialogRef.componentInstance.fIndex = pIndex;


    dialogRef.afterClosed().subscribe(result => {
      if (result !== undefined) {
        this.deleteFromArray(result);
      }
    });
  }

  deleteFromArray(index: any) {
    this.files.splice(index, 1);
  }

  formatBytes(bytes: any, decimals = 2) {
    if (!+bytes) return '0 Bytes'

    const k = 1024
    const dm = decimals < 0 ? 0 : decimals
    const sizes = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
  }
  editMaskTools(selectedTool: any) {
    console.log(selectedTool)
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
  onClickCampostion(selectedValue: any) {
    this.campostion = selectedValue
  }
  editEmailContent() {
    this.editEmailCont = this.textContent
  }
  loadEditImageCanvasComponent(img: any) {
    this.editImageSection = true;
    this.imageSrc = img.changingThisBreaksApplicationSecurity || img;
  }

  updateCanvasImage(base64String: any) {
    this.selectedImage = base64String;
    this.showEmailCopySave = true;
  }
  onClickSelect(image: any, id: any) {
    this.selectedImage = image.changingThisBreaksApplicationSecurity;
    this.selectButtonId = id;
  }

  // updateEmailContent(emailTextContent: any) {
  //   console.log(emailTextContent);
  //   this.textContent = emailTextContent;
  // }

  bulkEmail() {
    this.showProgress2 = true;
    let obj = {}
    if (this.uploadImageAssetsClicked) {
      obj = {
        "theme": this.selectedCampaignFromDropdown[0].data.theme,
        "audience": this.selectedCampaignFromDropdown[0].data.audiences.crm_data,
        "no_of_emails": 10,
      }
    } else {
      obj = {
        "theme": this.selectedCampaignFromDropdown[0].data.theme,
        "audience": this.selectedCampaignFromDropdown[0].data.audiences.crm_data,
        "image_context": this.contextVal + ", Aspect Ration: " + this.aspectsRatio + ", Color Tone:" + this.colorTone
          + ", Lighting:" + this.lighting + ", Composition:" + this.campostion + ", Content Type:" + this.ContentType,
        "no_of_emails": 10,
      }
    }
    this.emailService.bulkEmail(obj).subscribe((res: any) => {
      this.showProgress2 = false
      this.bulEmails = res.persionalized_emails
      this.ShowBulkEmailContents = true;
      this.bulEmailfiltered_DATA = res.persionalized_emails
      this.bulkEmailDisplay = res.persionalized_emails.email
      if (this.bulEmails.length > 1) {
        this.visibleEmails = this.bulEmails.slice(0, 3);
        this.showButtonBulkEMail = true;
        this.showSingleMailContent = false
        this.bulEmailTextContent = this.visibleEmails[0].text;
        this.bulEmailTextContentTranslate = this.visibleEmails[0].translation;
        this.bulkEmailLanguage = this.visibleEmails[0].language;
        if (this.visibleEmails[0].generated_image) {
          let base64_image = this.visibleEmails[0].generated_image
          base64_image = this.domSanitizer.bypassSecurityTrustResourceUrl('data:image/jpg;base64,'
            + this.visibleEmails[0].generated_image);
          this.bulkEmailImageContent = base64_image.changingThisBreaksApplicationSecurity;
        } else if (this.selectedImage) {
          this.bulkEmailImageContent = this.selectedImage.changingThisBreaksApplicationSecurity
        } else {
          this.bulkEmailImageContent = this.images[0].image
        }
        this.bulEmailTextContentEnglish = this.visibleEmails[0].text;
      } else {
        this.showSingleMailContent = true
      }
    });
  }

  showNext() {
    this.startIndex += 3;
    this.visibleEmails = this.bulEmails.slice(this.startIndex, this.startIndex + 3);
    this.activeEButton = this.activeEButton.fill(false)
  }

  showPrevious() {
    this.startIndex -= 3;
    this.visibleEmails = this.bulEmails.slice(this.startIndex, this.startIndex + 3);
    this.activeEButton = this.activeEButton.fill(false)
  }


  builEmailContents(ind: any, item: any) {
    this.selectedBulkEmailIndex = ind + this.startIndex
    this.bulEmailfiltered = this.bulEmailfiltered_DATA.filter(a => a.email === item.email)
    this.bulEmailfiltered.forEach((element: { data: any; text: any, translation: any, generated_image: any, language: any }) => {
      this.bulEmailTextContent = element.text;
      this.bulEmailTextContentTranslate = element.translation
      this.ShowBulkEmailContents = true;
      this.bulEmailTextContentEnglish = element.text
      this.activeEnglishButton = true;
      this.activeETranslatedButton = false
      this.activeEButton = this.activeEButton.fill(false);
      this.activeEButton[ind] = true
      if (element.generated_image) {
        let base64_image = element.generated_image
        base64_image = this.domSanitizer.bypassSecurityTrustResourceUrl('data:image/jpg;base64,'
          + element.generated_image);
        this.bulkEmailImageContent = base64_image.changingThisBreaksApplicationSecurity;
        // this.bulkEmailImageContent = `https://storage.googleapis.com/${this.bulkEmailImageContent}`;
      } else if (this.selectedImage) {
        this.bulkEmailImageContent = this.selectedImage.changingThisBreaksApplicationSecurity
      } else {
        this.bulkEmailImageContent = this.images[0].image

      }
      this.bulkEmailLanguage = element.language
    });
  }

  updateBulkEmailText(value: any) {
    this.bulEmails[this.selectedBulkEmailIndex].text = value;
  }

  updateEmailText(value: any) {
    this.textContent = value;
  }

  translated() {
    this.bulEmailTextContent = this.bulEmailTextContentTranslate
    this.activeEnglishButton = false
    this.activeETranslatedButton = true
  }

  english() {
    this.bulEmailTextContent = this.bulEmailTextContentEnglish
    this.activeEnglishButton = true
    this.activeETranslatedButton = false
  }

  showSaveButton(val: boolean) {
    this.showSaveBtn = val
  }
}
