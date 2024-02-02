
import { AfterViewInit, Component, ElementRef, EventEmitter, Input, OnChanges, Output, ViewChild } from '@angular/core';
import { CampaignNames } from '../email-copy/email-copy.component';
import { FormGroup, FormControl } from '@angular/forms';
import { EmailCopyService } from '../services/email-copy.service';
import { DomSanitizer } from '@angular/platform-browser';
import { BOLD_BUTTON, EditorConfig, FONT_SIZE_SELECT, FORE_COLOR, IMAGE_INPUT, INDENT_BUTTON, ITALIC_BUTTON, JUSTIFY_CENTER_BUTTON, JUSTIFY_FULL_BUTTON, JUSTIFY_LEFT_BUTTON, JUSTIFY_RIGHT_BUTTON, LINK_INPUT, ORDERED_LIST_BUTTON, OUTDENT_BUTTON, SEPARATOR, STRIKE_THROUGH_BUTTON, ST_BUTTONS, SUBSCRIPT_BUTTON, SUPERSCRIPT_BUTTON, UNDERLINE_BUTTON, UNDO_BUTTON, UNLINK_BUTTON, UNORDERED_LIST_BUTTON } from 'ngx-simple-text-editor';

@Component({
  selector: 'app-social-media-edit-canvas',
  templateUrl: './social-media-edit-canvas.component.html',
  styleUrl: './social-media-edit-canvas.component.scss'
})
export class SocialMediaEditCanvasComponent implements AfterViewInit, OnChanges {
  editImageSection: boolean = false;
  base64String: any;
  @Output() showSaveButton: EventEmitter<boolean> = new EventEmitter<boolean>();
  
  edit_mask_tools: CampaignNames[] = [{ name: "Rectangle" }, { name: "Brush" }, { name: "Circle" }, { name: "Move/Scale/Rotate" }];
  @ViewChild('myCanvas', { static: false })
  canvas!: ElementRef<HTMLCanvasElement> | any;

  @ViewChild('scream', { static: false })
  imgx!: ElementRef<HTMLImageElement> | any;

  private ctx!: CanvasRenderingContext2D | any;
  private img: HTMLImageElement = new Image();
  private isDrawing: boolean = false;
  private startX!: number;
  private startY!: number;

  uploadedEditImageForm = new FormGroup({
    selectedTool: new FormControl(),
    promptMsg: new FormControl(),
  });
  config: EditorConfig = {
    placeholder: 'Type something...',
    buttons: [UNDO_BUTTON, SEPARATOR, BOLD_BUTTON, ITALIC_BUTTON, UNDERLINE_BUTTON, STRIKE_THROUGH_BUTTON, JUSTIFY_LEFT_BUTTON, JUSTIFY_CENTER_BUTTON,
      JUSTIFY_RIGHT_BUTTON, JUSTIFY_FULL_BUTTON, ORDERED_LIST_BUTTON, UNORDERED_LIST_BUTTON, INDENT_BUTTON,
      OUTDENT_BUTTON, SUBSCRIPT_BUTTON, SUPERSCRIPT_BUTTON, FONT_SIZE_SELECT,
      LINK_INPUT, UNLINK_BUTTON, FORE_COLOR, IMAGE_INPUT]
  };
  @Input() imageSrc: any
  imageData: any;
  promptGeneratedImages!: any[];
  emailCopy!: any;
  showProgress: boolean = false;
  showImagesGenerated: boolean = false;

  image_base64: string | undefined;
  //Declare the property
  @Output() imageBase64Change: EventEmitter<any> = new EventEmitter<any>();
  //textContent

  @Output() emailTextContent: EventEmitter<any> = new EventEmitter<any>();

  @Input() selectedCampaignFromDropdown: any
  showEmailEditor: boolean = false;
  showGenerateImagesSpinner: boolean = false;

  textContent: string = "";
  showGenerateEmailBtn: boolean = false;
  selectedImage: any;
  showEmailCopySave: boolean = false;
  selectButtonId: any;
  maskedBase64String: any;
  selectDisable: boolean = false;
  //Raise the event to send the data back to parent

  constructor(public emailService: EmailCopyService, private domSanitizer: DomSanitizer,
  ) { }

  ngOnChanges() {
    /**********THIS FUNCTION WILL TRIGGER WHEN PARENT COMPONENT UPDATES 'someInput'**************/
    this.ngAfterViewInit();
  }

  editMaskTools(selectedTool: any) {
    console.log(selectedTool)
  }

  onMouseDown(event: MouseEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.buildMyCanvas();
    this.isDrawing = true;
    this.startX = event.clientX - this.canvas.nativeElement.getBoundingClientRect().left
    this.startY = event.clientY - this.canvas.nativeElement.getBoundingClientRect().top;

    var scaleX = this.canvas.nativeElement.width / this.canvas.nativeElement.getBoundingClientRect().width;
    var scaleY = this.canvas.nativeElement.height / this.canvas.nativeElement.getBoundingClientRect().height;
    this.startX *= scaleX;
    this.startY *= scaleY;
  }

  onMouseUp(event: MouseEvent): void {
    if (this.isDrawing) {
      event.preventDefault();
      event.stopPropagation();
      this.buildMyCanvas();

      var currentX = event.clientX - this.canvas.nativeElement.getBoundingClientRect().left;
      var currentY = event.clientY - this.canvas.nativeElement.getBoundingClientRect().top;

      var scaleX = this.canvas.nativeElement.width / this.canvas.nativeElement.getBoundingClientRect().width;
      var scaleY = this.canvas.nativeElement.height / this.canvas.nativeElement.getBoundingClientRect().height;
      currentX *= scaleX;
      currentY *= scaleY;

      const width = currentX - this.startX;
      const height = currentY - this.startY;

      if (width > 0 && height > 0) {
        this.ctx.strokeRect(this.startX, this.startY, width, height);
        this.isDrawing = false;
        this.imageData = this.ctx.getImageData(this.startX, this.startY, width, height);
        this.createMask()
      }
    }
  }
  createMask() {
    let srcImg = this.ctx.getImageData(0, 0, this.canvas.nativeElement.width, this.canvas.nativeElement.height)
    let destImg = this.ctx.createImageData(srcImg)
    let destData = destImg.data
    for (let i = 0; i < destData.length; i++) {
      destData[i] = 0;
    }

    let copyImageData = this.imageData;
    for (let i = 0; i < copyImageData.data.length; i++) {
      copyImageData.data[i] = 255;
    }
    let clone = this.canvas.nativeElement.cloneNode();
    let cloneCtx = clone.getContext('2d')
    cloneCtx.putImageData(destImg, 0, 0);
    cloneCtx.putImageData(copyImageData, this.startX, this.startY);
    var url = clone.toDataURL('image/jpeg');
    this.maskedBase64String = url.substring('data:image/jpeg;base64,'.length);
    console.log(this.maskedBase64String);
  }

  onMouseMove(event: MouseEvent): void {
    event.preventDefault();
    event.stopPropagation();
    if (!this.isDrawing) return;

    var currentX = event.clientX - this.canvas.nativeElement.getBoundingClientRect().left;
    var currentY = event.clientY - this.canvas.nativeElement.getBoundingClientRect().top;

    var scaleX = this.canvas.nativeElement.width / this.canvas.nativeElement.getBoundingClientRect().width;
    var scaleY = this.canvas.nativeElement.height / this.canvas.nativeElement.getBoundingClientRect().height;
    currentX *= scaleX;
    currentY *= scaleY;

    const width = currentX - this.startX;
    const height = currentY - this.startY;

    this.buildMyCanvas();
    this.ctx.strokeRect(this.startX, this.startY, width, height);
  }

  onMouseOut(event: MouseEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.buildMyCanvas();
  }

  private getBase64StringFromDataURL = (dataURL: any) =>
    dataURL.replace('data:', '').replace(/^.+,/, '');

  ngAfterViewInit() {
    const canvas: HTMLCanvasElement = this.canvas?.nativeElement;
    this.ctx = (canvas?.getContext('2d'));
    this.img.src = this.imageSrc
    this.img.onload = () => {
      this.ctx.clearRect(0, 0, this.img.width, this.img.height);
      this.drawImageScaled(this.img, this.ctx)
    };

    fetch(this.imageSrc)
      .then((res) => res.blob())
      .then((blob) => {
        // Read the Blob as DataURL using the FileReader API
        const reader = new FileReader();
        reader.onloadend = () => {
          // Convert to Base64 string
          this.base64String = this.getBase64StringFromDataURL(reader.result);
        };
        reader.readAsDataURL(blob);
      });
  }

  buildMyCanvas() {
    this.ctx.clearRect(0, 0, this.img.width, this.img.height);
    this.drawImageScaled(this.img, this.ctx)

    this.ctx.lineWidth = 1; // Border width
    this.ctx.strokeStyle = 'blue'; // Border color
  }

  drawImageScaled(img: HTMLImageElement, ctx: CanvasRenderingContext2D) {
    var canvas = ctx.canvas;
    window.devicePixelRatio = 2;
    var size = 378;

    canvas.style.width = size + "px";
    canvas.style.height = size + "px";
    var scale = window.devicePixelRatio;

    canvas.width = Math.floor(size * scale);
    canvas.height = Math.floor(size * scale);
    var hRatio = canvas.width / img.width;
    var vRatio = canvas.height / img.height;
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, img.width * hRatio, img.height * vRatio);
  }

  generate() {
    this.showGenerateImagesSpinner = true;
    let obj = {
      "prompt": this.uploadedEditImageForm.controls.promptMsg.value,
      "base_image_base64": this.base64String,
      "mask_base64": this.maskedBase64String
    }
    this.emailService.editImage(obj).subscribe((res: any) => {
      this.promptGeneratedImages = []
      res.generated_images.forEach((element: { images_base64_string: string; id: any }) => {
        this.emailCopy = this.domSanitizer.bypassSecurityTrustResourceUrl('data:image/jpg;base64,'
          + element.images_base64_string);
        this.promptGeneratedImages.push({ id: element.id, image: this.emailCopy });
        this.showGenerateImagesSpinner = false;
        this.showProgress = false;
        this.showImagesGenerated = true
      });
    })
  }

  onSelectImage(image: any, id: any) {
    this.showGenerateEmailBtn = true;
    this.showEmailEditor = true;
    this.selectButtonId = id;
    this.selectDisable = true;
    //emit imageBase64String to the parent component
    this.updatedImage(image);
  }

  updatedImage(image : any) {
    this.imageBase64Change.emit(image);
    // if(this.textContent){
    //   this.emailTextContent.emit(this.textContent);
    // }
  }

  onClickSelect(image: any) {
    this.selectedImage = image.changingThisBreaksApplicationSecurity;
    this.showSaveButton.emit(true);
    //this.selectButtonClick = true;
  }
}
