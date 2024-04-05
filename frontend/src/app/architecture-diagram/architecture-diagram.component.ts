import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-architecture-diagram',
  templateUrl: './architecture-diagram.component.html',
  styleUrl: './architecture-diagram.component.scss'
})
export class ArchitectureDiagramComponent {
  constructor(public dialog:MatDialog){

  }

  close(): void {
    const dialogRef = this.dialog.closeAll()
}
}
