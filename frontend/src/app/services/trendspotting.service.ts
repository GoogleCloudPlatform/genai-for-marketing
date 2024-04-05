import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { catchError, throwError } from 'rxjs';
import { environment } from '../../environments/environments';

@Injectable({
  providedIn: 'root'
})
export class TrendspottingService {

  constructor(public http: HttpClient , public snackBar: MatSnackBar) { }

  getTopSearchedTerms(date: any) {
    return this.http
      .get(`${environment.apiUrl}/get-top-search-terms/${date}`)
      .pipe(
        catchError(this.handleError)
      );
  }

  postSummarizeNews(query: any) {
    const head = new HttpHeaders().set('content-type', 'application/json')
    let options = {
      headers: head
    }
    return this.http
      .post(`${environment.apiUrl}/post-summarize-news`, query , options)
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {

      console.error('An error occurred:', error.error);

      this.showSnackbarCssStyles(error.error, 'Close', '4000')
    } else {

      this.showSnackbarCssStyles(error?.message, 'Close', '4000')
      // console.error(
      //   `Backend returned code ${error.status}, ` +
      //   `body was: ${error.error}`);
    }

    return throwError(
      'Something bad happened; please try again later.');
  }
  consumerInsightsSearch(query: any) {
    const head = new HttpHeaders().set('content-type', 'application/json')
    let options = {
      headers: head
    }
    return this.http.post(`${environment.apiUrl}/post-consumer-insights`, query, options)
      .pipe(catchError(this.handleError));
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
