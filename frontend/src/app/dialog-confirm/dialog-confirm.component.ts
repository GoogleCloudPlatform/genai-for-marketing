import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-dialog-confirm',
  templateUrl: './dialog-confirm.component.html',
  styleUrl: './dialog-confirm.component.scss'
})
export class DialogConfirmComponent {

  public fName!: string;
  public fIndex: any;

  constructor(private modalRef: MatDialogRef<DialogConfirmComponent>) { }

  ngOnInit() {
  }

  confirm() {
    this.modalRef.close(this.fIndex);
  }
  cancel() {
    this.modalRef.close();
  }
}
