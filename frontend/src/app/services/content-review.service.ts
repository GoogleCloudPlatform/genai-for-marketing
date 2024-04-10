import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { catchError, throwError } from 'rxjs';
import { environment } from '../../environments/environments';

@Injectable({
  providedIn: 'root'
})
export class ContentReviewService {

  constructor(public http: HttpClient, public snackBar: MatSnackBar) { }

  export(query: any, userId: string, campaignId: string) {
    const head = new HttpHeaders().set('content-type', 'application/json')
    let options = {
      headers: head
    }
    return this.http.post(`${environment.apiUrl}/export-google-doc`, query, options)
      .pipe(catchError(this.handleError));

  }

  exportToGoogleSlides(folderId: any) {
    const head = new HttpHeaders().set('content-type', 'application/json')
    let options = {
      headers: head
    }
    return this.http.post(`${environment.apiUrl}/creative-slides-upload`, folderId, options)
      .pipe(catchError(this.handleError));

  }

  getActivation(query: any, userId: string, campaignId: string) {
    const head = new HttpHeaders().set('content-type', 'application/json')
    let options = {
      headers: head
    }
    return this.http.put(`${environment.apiUrl}/users/${userId}/campaigns/${campaignId}/status/`, query, options)
      .pipe(catchError(this.handleError));

  }
  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {

      console.error('An error occurred:', error.error);
      this.showSnackbarCssStyles(error.error, 'Close', '4000')

    } else {

      this.showSnackbarCssStyles(error?.message, 'Close', '4000')
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
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
}
