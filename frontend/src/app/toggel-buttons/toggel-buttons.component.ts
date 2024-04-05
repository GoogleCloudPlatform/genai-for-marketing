import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ArchitectureDiagramComponent } from '../architecture-diagram/architecture-diagram.component';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-toggel-buttons',
  templateUrl: './toggel-buttons.component.html',
  styleUrl: './toggel-buttons.component.scss'
})
export class ToggelButtonsComponent {
  photoURL: string | undefined;
  subscription: Subscription | undefined;
  // constructor(public dialog:MatDialog){}
  constructor(public _router: Router, public loginService: LoginService, public dialog: MatDialog) {
    this.subscription = this.loginService.getUserDetails().subscribe(message => {
      this.photoURL = message?.photoURL
    });
  }
  showArchitetureDig(): void {
    const dialogRef = this.dialog.open(ArchitectureDiagramComponent, {
      disableClose: true, height: "auto"
    });
  }
  navigateToUserJourney() {
    this._router.navigate(['user-journey'])
  }
}
