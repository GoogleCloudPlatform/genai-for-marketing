import { Component } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CampaignNames } from '../email-copy/email-copy.component';
import { AudiencesService } from '../services/audiences.service';
import { CampaignService } from '../services/campaign.service';
import { EmailCopyService } from '../services/email-copy.service';
import { LoginService } from '../services/login.service';
import { ContentReviewService } from '../services/content-review.service';
import { DomSanitizer } from '@angular/platform-browser';
import { BOLD_BUTTON, CUSTOM, EditorConfig, FONT_SIZE_SELECT, FORE_COLOR, IMAGE_INPUT, INDENT_BUTTON, ITALIC_BUTTON, JUSTIFY_CENTER_BUTTON, JUSTIFY_FULL_BUTTON, JUSTIFY_LEFT_BUTTON, JUSTIFY_RIGHT_BUTTON, LINK_INPUT, ORDERED_LIST_BUTTON, OUTDENT_BUTTON, SEPARATOR, STRIKE_THROUGH_BUTTON, ST_BUTTONS, SUBSCRIPT_BUTTON, SUPERSCRIPT_BUTTON, UNDERLINE_BUTTON, UNDO_BUTTON, UNLINK_BUTTON, UNORDERED_LIST_BUTTON } from 'ngx-simple-text-editor';


@Component({
  selector: 'app-content-review',
  templateUrl: './content-review.component.html',
  styleUrl: './content-review.component.scss'
})
export class ContentReviewComponent {

  showHeadline: boolean = false;
  assetGroupPmaxForm = new FormGroup({
    selectedTool: new FormControl(),
    promptMsg: new FormControl(),
  });
  config: EditorConfig = {
    placeholder: 'Type something...',
    buttons: [UNDO_BUTTON, SEPARATOR, BOLD_BUTTON, ITALIC_BUTTON, UNDERLINE_BUTTON, STRIKE_THROUGH_BUTTON, JUSTIFY_LEFT_BUTTON, JUSTIFY_CENTER_BUTTON,
      JUSTIFY_RIGHT_BUTTON, JUSTIFY_FULL_BUTTON, ORDERED_LIST_BUTTON, UNORDERED_LIST_BUTTON, INDENT_BUTTON,
      OUTDENT_BUTTON, FONT_SIZE_SELECT,
      LINK_INPUT, UNLINK_BUTTON, FORE_COLOR]
  };
  startIndex: any = 0;
  activeEButton: boolean[] = [true, false, false];
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
  campaignId: any;
  folderId: any;
  text: any
  fileUrl: any;
  activationSatus: any;
  activateButton: any = { 'emails': false, 'website_post': false, 'ads_insta': false, 'ads_threads': false, 'asset_classes_text': false };
  exploreFiles: any;
  showExportFileLink: boolean = false;
  public items: any = [{ id: 0, name: 'Google Drive' }];
  selectedOption = 0;
  visibleEmails: any;
  bulEmails: any;
  bulEmailTextContent: any;
  bulEmailfiltered_DATA: any;
  bulEmailfiltered: any;
  ShowBulkEmailContents: boolean = false;
  showButtonBulkEMail: boolean = false;
  bulEmailTextContentTraslate!: any;
  bulEmailTextContentEnglish!: any;
  activeEnglishButton: boolean = true
  activeETranslatedButton: boolean = false
  bulkEmailImageContent: string = '';
  bulkEmailLanguage: any;

  constructor(public loginService: LoginService, public audiencesSerive: AudiencesService, public snackBar: MatSnackBar,
    public emailService: EmailCopyService, public contentReview: ContentReviewService,
    public campaignServ: CampaignService, private sanitizer: DomSanitizer) {
    this.loginService.getUserDetails().subscribe(res => {
      this.userLoggedIn = true;
      this.photoURL = res?.photoURL;
      this.userId = res?.uid
    });
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
      // this.selectedCampaignFromDropdown = [this.campaignResults[0]]
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

  onClickCampaign(selectedValue: any) {
    this.filtered = this.CAMPAIGN_DATA1.filter(a => a.data.name.trim() === selectedValue.trim())
    this.clearOnSelectCampaign()
    this.filtered.forEach((element: { data: any; id: any }) => {
      this.selectedCampaignId = element.id;
      this.campaignData = element.data;
      this.selectedCampaignFromDropdown = this.campaignResults.filter((c: any) => c.id === this.selectedCampaignId);
      this.campaignId = element.id;
      this.folderId = element.data.workspace_assets?.new_folder_id
      this.text = element.data.emails?.text;
      this.visibleEmails = element.data.emails?.persionalized_emails;
      this.bulEmails = element.data.emails?.persionalized_emails;
      this.bulEmailfiltered_DATA = element.data.emails?.persionalized_emails
      this.activeEButton = [true, false, false];

      if (this.bulEmails?.length > 0) {
        this.visibleEmails = this.bulEmails.slice(0, 3);
        this.bulkEmailImageContent = `https://storage.mtls.cloud.google.com/${this.visibleEmails[0].gcs_path}`
        this.bulEmailTextContent = this.visibleEmails[0].text;
        this.bulEmailTextContentTraslate = this.visibleEmails[0].translation
        this.bulkEmailLanguage = this.visibleEmails[0].language
      } else {
        this.bulEmailTextContent = element.data.emails?.text;
        this.bulkEmailImageContent = `https://storage.mtls.cloud.google.com/${element.data.emails?.gcs_path}`

      }
      this.activationSatus = element.data.status
      this.exploreFiles = `http://drive.google.com/corp/drive/folders/${element.data.workspace_assets.new_folder_id}/`
      this.showExportFileLink = true
      if (this.campaignData.emails != null) {
        if ('status' in this.campaignData.emails) {
          this.activateButton['emails'] = true
        }
      }
      if (this.campaignData.website_post != null) {
        if ('status' in this.campaignData.website_post) {
          this.activateButton['website_post'] = true
        }
      }
      if (this.campaignData.ads_insta != null) {
        if ('status' in this.campaignData.ads_insta) {
          this.activateButton['ads_insta'] = true
        }
      }
      if (this.campaignData.ads_threads != null) {
        if ('status' in this.campaignData.ads_threads) {
          this.activateButton['ads_threads'] = true
        }
      }
      if (this.campaignData.asset_classes_text != null) {
        if ('status' in this.campaignData.asset_classes_text) {
          this.activateButton['asset_classes_text'] = true
        }
      }
    });
  }

  export(docName: any, textData: any, image_prefix: any, images: any) {
    let obj = {
      "folder_id": this.folderId,
      "doc_name": docName,
      "text": textData,
      "image_prefix": image_prefix,
      "images": images
    }
    this.contentReview.export(obj, this.userId, this.campaignId).subscribe((res: any) => {
      this.showExportFileLink = true
      //const data = res.doc_id
      // const blob = new Blob([data], { type: 'application/octet-stream' });
      // this.fileUrl = this.sanitizer.bypassSecurityTrustResourceUrl(window.URL.createObjectURL(blob));

    });
  }

  exportEmails(docName: any, textData: any, image_prefix: any, images: any) {
    let gcs_paths = [];

    for (let i = 0; i < images.length; i++) {
      gcs_paths.push(images[i].gcs_path)
    }
    let persionalized_emails = this.selectedCampaignFromDropdown[0].data.emails.persionalized_emails;
    let concatenated_text = '';
    for (let i = 0; i < persionalized_emails.length; i++) {
      concatenated_text = concatenated_text + '\n' + persionalized_emails[i].email + '\n' + persionalized_emails[i].first_name + '\n' + persionalized_emails[i].text + '\n' + persionalized_emails[i].translation + '\n\n';
    }
    let obj = {
      "folder_id": this.folderId,
      "doc_name": docName,
      "text": textData + '\n' + concatenated_text,
      "image_prefix": image_prefix,
      "images": gcs_paths
    }
    this.contentReview.export(obj, this.userId, this.campaignId).subscribe((res: any) => {
      this.showExportFileLink = true
    });
  }
  exportToGoogleSlides() {

    let obj = {
      "folder_id": this.folderId,
    }
    this.contentReview.exportToGoogleSlides(obj).subscribe((res: any) => {
      this.showSnackbar("Google Slides Exported Successfully", 'Close', '2000')
    });
  }
  onClickActive(key: any) {
    let obj = {
      "key": key,
      "status": 'Activated'
    }
    this.contentReview.getActivation(obj, this.userId, this.campaignId).subscribe((res: any) => {
      this.activateButton[key] = true
      this.showSnackbar(res?.message, 'Close', '1000')
    });
  }

  clearOnSelectCampaign() {
    this.activateButton = { 'emails': false, 'website_post': false, 'ads_insta': false, 'ads_threads': false, 'asset_classes_text': false }
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

  builEmailContents(ind: any, item: any) {
    this.bulEmailfiltered = this.bulEmailfiltered_DATA.filter((a: any) => a.email === item.email)
    this.bulEmailfiltered.forEach((element: { data: any; text: any, translation: any, gcs_path: any, language: any }) => {
      this.bulEmailTextContent = element.text;
      this.bulkEmailImageContent = `https://storage.mtls.cloud.google.com/${element.gcs_path}`
      this.bulEmailTextContentTraslate = element.translation
      this.ShowBulkEmailContents = true;
      this.bulEmailTextContentEnglish = element.text
      this.activeEnglishButton = true;
      this.bulkEmailLanguage = element.language
      this.activeETranslatedButton = false
      this.activeEButton = this.activeEButton.fill(false)
      this.activeEButton[ind] = true

    });
  }

  translated() {
    this.bulEmailTextContent = this.bulEmailTextContentTraslate
    this.activeEnglishButton = false
    this.activeETranslatedButton = true
  }

  english() {
    this.bulEmailTextContent = this.bulEmailTextContentEnglish
    this.activeEnglishButton = true
    this.activeETranslatedButton = false
  }
}
