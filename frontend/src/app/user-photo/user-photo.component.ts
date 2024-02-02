import { AfterViewInit, Component, Inject, OnDestroy, inject } from '@angular/core';
import { Router } from '@angular/router';
import { LoginButtonComponent } from '../login-button/login-button.component';
import { Subscription } from 'rxjs';
import { Dialog } from '@angular/cdk/dialog';
import { Auth, User, user } from '@angular/fire/auth';
import { LoginService } from '../services/login.service';

@Component({
  selector: 'app-user-photo',
  templateUrl: './user-photo.component.html',
  styleUrl: './user-photo.component.scss',
  //providers :[Auth]
  //standalone: true,
})
export class UserPhotoComponent implements OnDestroy, AfterViewInit {
  photoURL: string | undefined;
  subscription: Subscription | undefined;
  userLoggedIn: boolean = false;
  private auth: Auth = inject(Auth);
  user$ = user(this.auth);
  userSubscription: Subscription;

  constructor(private _router: Router, public dialog: Dialog, public loginService: LoginService) {
    this.userSubscription = this.user$.subscribe((aUser: User | null) => {
      //handle user state changes here. Note, that user will be null if there is no currently logged in user
      if (aUser) {
        this.dialog.closeAll();
        this.userLoggedIn = true;
        this.loginService.sendUserDetails(aUser)
        if (aUser.photoURL) {
          this.photoURL = aUser.photoURL;
        }
      }
      else {
        this.userLoggedIn = false;
        this.ngAfterViewInit()
      }
    })
  }

  ngAfterViewInit() {
    if (!this.photoURL) {
      this.showLogIn()
    }
  }

  navigateToUserJourney() {
    this.userLoggedIn = true;
    this._router.navigate(['user-journey'])
  }


  showLogIn(): void {
    this.dialog.open(LoginButtonComponent, {
      disableClose: true,
      width: '350px',
      panelClass: 'login-container'
    });
  }

  ngOnDestroy() {
    // when manually subscribing to an observable remember to unsubscribe in ngOnDestroy
    this.userSubscription.unsubscribe();
  }
}
