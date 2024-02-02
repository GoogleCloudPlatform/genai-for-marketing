import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ImageMaskService {
  private maskedImageSubject = new BehaviorSubject<string>('');

  createMask(userInput: any): void {
    const img = new ImageData(userInput.image_width, userInput.image_height);

    for (let i = userInput.mask_start_x; i < userInput.mask_end_x; i++) {
      for (let j = userInput.mask_start_y; j < userInput.mask_end_y; j++) {
        const index = (j * img.width + i) * 4;
        img.data[index] = 255; // Red channel
        img.data[index + 1] = 255; // Green channel
        img.data[index + 2] = 255; // Blue channel
        img.data[index + 3] = 255; // Alpha channel
      }
    }

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = img.width;
    canvas.height = img.height;
    ctx!.putImageData(img, 0, 0);

    const maskedImage = canvas.toDataURL('image/jpeg');

    this.maskedImageSubject.next(maskedImage);
  }

  getMaskedImage(): Observable<string> {
    return this.maskedImageSubject.asObservable();
  }
}



  // maskedImage: string = '';
  // private subscription: Subscription;

  // constructor(private imageMaskService: ImageMaskService) {
  //   this.subscription = this.imageMaskService.getMaskedImage().subscribe((maskedImage) => {
  //     this.maskedImage = maskedImage;
  //   });
  // }
  // @ViewChild('myCanvas') canvas!: ElementRef<HTMLCanvasElement>;
  // private ctx!: CanvasRenderingContext2D | any;
  // private img!: HTMLImageElement | any;
  // private base64String!: string;

  // private offsetX!: number;
  // private offsetY!: number;
  // private isDown: boolean = false;
  // private startX: number = 0;
  // private startY: number = 0;
  // private endX: number = 0;
  // private endY: number = 0;

  // private prevStartX: number = 0;
  // private prevStartY: number = 0;
  // private prevWidth: number = 0;
  // private prevHeight: number = 0;

  // ngAfterViewInit() {

  //   const canvas: HTMLCanvasElement = this.canvas?.nativeElement;
  //   //   this.ctx = (canvas?.getContext('2d'));
  //   this.ctx = canvas.getContext('2d');
  //   this.img = new Image();
  //   this.img.src = this.imageSrc;
  //   console.log(this.img)

  //   this.img.onload = () => {
  //     this.canvas.nativeElement.style.height = this.img.height + 'px';
  //     this.canvas.nativeElement.style.width = this.img.width + 'px';
  //     this.canvas.nativeElement.height = this.img.height;
  //     this.canvas.nativeElement.width = this.img.width;

  //     this.ctx.clearRect(0, 0, this.canvas.nativeElement.width, this.canvas.nativeElement.height);
  //     this.ctx.drawImage(this.img, 0, 0);

  //     this.ctx.strokeStyle = 'blue';
  //     this.ctx.lineWidth = 2;
  //   };
  // }

  // loadFile(event: any): void {
  //   this.img.src = URL.createObjectURL(event.target.files[0]);
  //   this.img.onload = () => {
  //     this.drawCanvasImage();
  //   };

  //   let reader = new FileReader();
  //   reader.onload = () => {
  //     this.base64String = reader.result?.toString().replace('data:', '').replace(/^.+,/, '');
  //   };
  //   reader.readAsDataURL(event.target.files[0]);
  // }

  // drawCanvasImage(): void {
  //   this.canvas.nativeElement.style.height = this.img.height + 'px';
  //   this.canvas.nativeElement.style.width = this.img.width + 'px';
  //   this.canvas.nativeElement.height = this.img.height;
  //   this.canvas.nativeElement.width = this.img.width;

  //   this.ctx.clearRect(0, 0, this.canvas.nativeElement.width, this.canvas.nativeElement.height);
  //   this.ctx.drawImage(this.img, 0, 0);

  //   this.ctx.strokeStyle = 'blue';
  //   this.ctx.lineWidth = 2;
  // }

  // handleMouseDown(e: MouseEvent): void {
  //   e.preventDefault();
  //   e.stopPropagation();

  //   this.drawCanvasImage();

  //   this.startX = (e.clientX - this.offsetX);
  //   this.startY = (e.clientY - this.offsetY + window.pageYOffset);

  //   this.isDown = true;
  // }

  // handleMouseUp(e: MouseEvent): void {
  //   e.preventDefault();
  //   e.stopPropagation();

  //   this.isDown = false;

  //   this.drawCanvasImage();

  //   this.ctx.strokeRect(this.prevStartX, this.prevStartY, this.prevWidth, this.prevHeight);

  //   this.startX = this.prevStartX;
  //   this.startY = this.prevStartY;
  //   this.endX = this.prevStartX + this.prevWidth;
  //   this.endY = this.prevStartY + this.prevHeight;

  //   this.prevStartX = 0;
  //   this.prevStartY = 0;
  //   this.prevWidth = 0;
  //   this.prevHeight = 0;
  // }

  // handleMouseOut(e: MouseEvent): void {
  //   e.preventDefault();
  //   e.stopPropagation();

  //   this.isDown = false;
  // }

  // handleMouseMove(e: MouseEvent): void {
  //   e.preventDefault();
  //   e.stopPropagation();

  //   if (!this.isDown) {
  //     return;
  //   }

  //   const mouseX = (e.clientX - this.offsetX);
  //   const mouseY = (e.clientY - this.offsetY + window.pageYOffset);

  //   this.drawCanvasImage();

  //   const width = mouseX - this.startX;
  //   const height = mouseY - this.startY;

  //   this.ctx.strokeRect(this.startX, this.startY, width, height);

  //   this.prevStartX = this.startX;
  //   this.prevStartY = this.startY;
  //   this.prevWidth = width;
  //   this.prevHeight = height;
  // }
  // applyMask(userInput: any): void {
  //   this.imageMaskService.createMask(userInput);
  // }