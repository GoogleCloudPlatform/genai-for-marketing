import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import { SelectionModel } from '@angular/cdk/collections';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { Sort, MatSortModule, MatSort, } from '@angular/material/sort';
import { CampaignService } from '../services/campaign.service';
import { LoginService } from '../services/login.service';
import { SortEvent } from 'primeng/api/sortevent';
import { MenuItem, MessageService, PrimeNGConfig } from 'primeng/api';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Table } from 'primeng/table';
import { DomSanitizer } from '@angular/platform-browser';
import { AudiencesService } from '../services/audiences.service';

export interface PeriodicElement {
  name: string;
  theme: string;
  status: string;
  doc_id: string;
  id: string;
}

@Component({
  selector: 'app-campaign-list',
  templateUrl: './campaign-list.component.html',
  styleUrl: './campaign-list.component.scss',
  providers: [MessageService]
})
export class CampaignListComponent implements AfterViewInit{
  @ViewChild("docPreview")
  private docPreviewDiv!: ElementRef<HTMLElement>;

  @ViewChild('dt') table!: Table;

  @ViewChild(MatPaginator)
  paginator!: MatPaginator;

  @ViewChild(MatSort, { static: false })
  sort!: MatSort;
  menuitems!: MenuItem[];
  displayedColumns: string[] = ['select', 'name', 'theme', 'status', 'actions'];
  ELEMENT_DATA: PeriodicElement[] = [];
  selection = new SelectionModel<PeriodicElement>(true, []);
  userId: any;
  dataSource!: MatTableDataSource<PeriodicElement>;
  campaignResults: any[] = [];
  showchatboot: boolean = false;
  photoURL: any;
  selectedItems!: any;
  docPreviewUrl: any;
  editBrief: any;
  exploreFiles: any;
  showProgress: boolean = false;
  imagePreview: boolean = false;
  imageSrc: any;
  saveCampaignId: any;
  userLoggedIn: boolean = false
  activeitem: any;
  showUploadSpinner: boolean = false;
  checkedCampaignRowId: any;
  disableCheckboxes: boolean = false;
  enableCampaignId: any;
  constructor(public campaignServ: CampaignService, public audiencesSerive: AudiencesService, private sanitizer: DomSanitizer, private snackBar: MatSnackBar, public loginService: LoginService, private messageService: MessageService, private primengConfig: PrimeNGConfig) {
    this.loginService.getUserDetails().subscribe(res => {
      this.userId = res?.uid;
      this.photoURL = res?.photoURL;
      this.userLoggedIn = true;
    });
  }

  ngAfterViewInit() {
    this.docPreviewDiv!?.nativeElement?.scrollIntoView({
      behavior: "smooth",
      block: "start",
      inline: "nearest"
    });
  }
  ngOnInit() {
    this.campaignServ.getCampaigns(this.userId).subscribe((res: any) => {
      this.campaignResults = res.results;
      this.ELEMENT_DATA = this.campaignResults?.map((res: any) => {
        return { name: res.data.name, theme: res.data.theme, status: res.data.status, doc_id: res.data.workspace_assets, id: res.id };
      })
    });
    this.menuitems = [{
      items: [{

        icon: 'pi pi-upload',
        command: () => {
          this.update(this.selectedItems);
        }
      },
      {

        icon: 'pi pi-fw pi-trash',
        command: () => {
          this.deleteProduct(this.selectedItems);
        }
      }
      ]
    }
    ];
  }
  getMenuItemsForItem(selectedProduct: any) {
    return this.menuitems = [{
      items: [{

        icon: 'pi pi-fw pi-pencil',
        command: () => {
          this.update(selectedProduct);
        }
      },
      {

        icon: 'pi pi-fw pi-trash',
        command: () => {
          this.deleteProduct(selectedProduct);
        }
      }
      ]
    }
    ];
  }
  update(selectedProduct: any) {
    this.messageService.add({ severity: 'success', summary: 'Success', detail: 'Data Updated' });
  }

  onClickMarketingAssi() {
    this.showchatboot = true
  }

  customSort(event: SortEvent) {
    event?.data?.sort((data1, data2) => {
      let value1 = data1[event?.field!];
      let value2 = data2[event?.field!];
      let result = null;

      if (value1 == null && value2 != null) result = -1;
      else if (value1 != null && value2 == null) result = 1;
      else if (value1 == null && value2 == null) result = 0;
      else if (typeof value1 === 'string' && typeof value2 === 'string') result = value1.localeCompare(value2);
      else result = value1 < value2 ? -1 : value1 > value2 ? 1 : 0;

      return event?.order! * result;
    });
  }

  deleteProduct(product: any) {
    this.campaignServ.deleteCampaign(this.userId, product.id).subscribe((res: any) => {
      this.showSnackbarCssStyles(res?.message, 'Close', '4000')
    })
  }
  showSnackbarCssStyles(content: any, action: any, duration: any) {
    let sb = this.snackBar.open(content, action, {
      duration: duration,
      panelClass: ["custom-style"]
    });
    sb.onAction().subscribe(() => {
      sb.dismiss();
    });
    this.campaignServ.getCampaigns(this.userId).subscribe((res: any) => {
      this.campaignResults = res.results;
      this.ELEMENT_DATA = this.campaignResults?.map((res: any) => {
        return { name: res.data.name, theme: res.data.theme, status: res.data.status, doc_id: res.data.workspace_assets, id: res.id };
      })
    })
  }
  selectedProduct(product: any) {
    this.showProgress = true;
    this.docPreviewUrl = `https://drive.google.com/file/d/${product?.doc_id?.doc_id}/preview`;
    this.editBrief = `https://docs.google.com/document/d/${product?.doc_id?.doc_id}/edit`;
    this.exploreFiles = `http://drive.google.com/corp/drive/folders/${product?.doc_id?.new_folder_id}/`;
    this.showProgress = false;
  }

  imageUpload(imageInput: any, product: any , ind : any) {
    this.showUploadSpinner = true;
    this.checkedCampaignRowId = ind
    const folder_id = product.doc_id.new_folder_id
    const file: File = imageInput.files[0];
    const reader = new FileReader();
    reader.addEventListener('load', (event: any) => {
      this.campaignServ.imageUpload(file, folder_id, event).subscribe((res: any) => {
        this.saveCampaignId = res;
        this.imageSrc = event.target.value
        this.imagePreview = true;
        this.saveToCampaign(product, this.saveCampaignId)
      })
    });
    reader.readAsDataURL(file);
  }
  saveToCampaign(product: any, saveCampaignId: any) {
    let selectedCampaign = this.campaignResults.filter((c: any) => c.id === product.id);
    //  selectedCampaign[0].data.trendspotting_summaries = this.summarizeNewsResults
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
      "campaign_uploaded_images": { saveCampaignId },
      "status": selectedCampaign[0].data.status
    }
    this.audiencesSerive.updateCampaign(obj, this.userId, product.id).subscribe((res: any) => {
      this.showSnackbarCssStyles(res?.message, 'Close', '4000');
      this.showUploadSpinner = false
    });
  }


  onSelection(i: any, product: any, checked: any) {
    if (checked) {
      this.showProgress = true;
      this.docPreviewUrl = `https://drive.google.com/file/d/${product?.doc_id?.doc_id}/preview`;
      this.editBrief = `https://docs.google.com/document/d/${product?.doc_id?.doc_id}/edit`;
      this.exploreFiles = `http://drive.google.com/corp/drive/folders/${product?.doc_id?.new_folder_id}/`;
      this.showProgress = false;
      this.ngAfterViewInit()
      this.showSnackbar("Campaign selected! Scroll down to view the doc preview ! ", 'Close', '4000')
    } else{
      this.disableCheckboxes = false;
    }
  }

  onNameSelection(i: any, product: any) {
    let campaignName = product.name
    this.showProgress = true;
    this.docPreviewUrl = `https://drive.google.com/file/d/${product?.doc_id?.doc_id}/preview`;
    this.editBrief = `https://docs.google.com/document/d/${product?.doc_id?.doc_id}/edit`;
    this.exploreFiles = `http://drive.google.com/corp/drive/folders/${product?.doc_id?.new_folder_id}/`;
    this.showProgress = false;
    this.ngAfterViewInit();
    this.showSnackbar(`Campaign: ${campaignName} selected! Scroll down to view the doc preview !`, 'Close', '4000')
  }

  showSnackbar(content: any, action: any, duration: any) {
    let sb = this.snackBar.open(content, action, {
      duration: duration,
    });
    sb.onAction().subscribe(() => {
      sb.dismiss();
    });
  }

  onRowSelect(event: any) {
    // this.messageService.add({severity:'info', summary:'Product Selected', detail: event.data.name});
  }

  onRowUnselect(event: any) {
    //this.messageService.add({severity:'info', summary:'Product Unselected',  detail: event.data.name});
  }
}
