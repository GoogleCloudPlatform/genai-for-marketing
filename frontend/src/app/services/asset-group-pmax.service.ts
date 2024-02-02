import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { catchError, throwError } from 'rxjs';
import { environment } from '../../environments/environments';

@Injectable({
  providedIn: 'root'
})
export class AssetGroupPmaxService {

  constructor(public http: HttpClient, public snackBar: MatSnackBar) { }

  generateImages(obj: any) {
    const head = new HttpHeaders().set('content-type', 'application/json')
    let options = {
      headers: head
    }

    return this.http.post(`${environment.apiUrl}/generate-image`, obj, options)

      .pipe(catchError((error: HttpErrorResponse) => this.handleError(error, this)));

  }

  generateTextContents(obj: any) {
    const head = new HttpHeaders().set('content-type', 'application/json')
    let options = {
      headers: head
    }

    return this.http.post(`${environment.apiUrl}/generate-content`, obj, options)
      .pipe(catchError((error: HttpErrorResponse) => this.handleError(error, this)));

  }

  handleError(error: HttpErrorResponse, service: AssetGroupPmaxService) {
    if (error.error instanceof ErrorEvent) {

      console.error('An error occurred:', error.error);

      service.showSnackbarCssStyles(error.error, 'Close', '4000')
    } else {

      service.showSnackbarCssStyles(error.message || "Error", 'Close', '4000')
    }
    return throwError(
      'Something bad happened; please try again later.');
  }

  showSnackbarCssStyles(content: any, action: any, duration: any) {
    let sb = this.snackBar.open(content, action, {
      duration: duration,
      panelClass: ["custom-style"]
    });
    sb.onAction().subscribe(() => {
      sb.dismiss();
    });
  }


  updateCampaignWebsitePost(query: any, userId: string, campaignId: string) {
    const head = new HttpHeaders().set('content-type', 'application/json')
    let options = {
      headers: head
    }
    return this.http.put(`${environment.apiUrl}/users/${userId}/campaigns/${campaignId}`, query, options)
      .pipe(catchError((error: HttpErrorResponse) => this.handleError(error, this)));

  }
}
