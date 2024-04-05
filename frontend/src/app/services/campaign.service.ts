import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { catchError, throwError } from 'rxjs';
import { environment } from '../../environments/environments';

@Injectable({
  providedIn: 'root'
})
export class CampaignService {

  constructor(public http: HttpClient, public snackBar: MatSnackBar) { }

  createCampaign(query: any, userId: string) {
    const head = new HttpHeaders().set('content-type', 'application/json')
    let options = {
      headers: head
    }
    return this.http.post(`${environment.apiUrl}/users/${userId}/campaigns`, query, options)
      .pipe(catchError(this.handleError));

  }

  updateCampaign(query: any, userId: string, campaignId: string) {
    const head = new HttpHeaders().set('content-type', 'application/json')
    let options = {
      headers: head
    }
    return this.http.post(`${environment.apiUrl}/users/${userId}/campaigns/${campaignId}`, query, options)
      .pipe(catchError(this.handleError));

  }

  imageUpload(file: any, folder_id: string, event: any) {
    const formData = new FormData();
    formData.append('file', file, file.name);
    return this.http.post(`${environment.apiUrl}/post-upload-file-drive/${folder_id}`, formData)
      .pipe(catchError(this.handleError));
  }

  imageUploadToGCS(file: any, folder_id: string, event: any) {
    const formData = new FormData();
    formData.append('file', file, file.name);
    return this.http.post(`${environment.apiUrl}/post-upload-file-gcs/${folder_id}`, formData)
      .pipe(catchError(this.handleError));
  }
  getCampaigns(userId: string) {
    return this.http
      .get(`${environment.apiUrl}/users/${userId}/campaigns`)
      .pipe(
        catchError(this.handleError)
      );
  }

  getCampaign(userId: string, campaignId: string) {
    //xuBZNiigPqSt0ZpprUPyfbQpdFR2
    return this.http
      .get(`${environment.apiUrl}/users/${userId}/campaigns/${campaignId}`)
      .pipe(
        catchError(this.handleError)
      );
  }

  deleteCampaign(userId: string, campaignId: string) {
    return this.http
      .delete(`${environment.apiUrl}/users/${userId}/campaigns/${campaignId}`)
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      console.error('An error occurred:', error.error);
      //  this.showSnackbarCssStyles(error.error, 'Close', '4000')
    } else {

      //   this.showSnackbarCssStyles(error?.message, 'Close', '4000')
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

  dataURLtoFile(dataurl: any, filename: any) {
    var arr = dataurl.split(','),
      mime = arr[0].match(/:(.*?);/)[1],
      bstr = atob(arr[arr.length - 1]),
      n = bstr.length,
      u8arr = new Uint8Array(n);
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, { type: mime });
  }
}
