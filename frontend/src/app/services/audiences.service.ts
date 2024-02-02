
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';
import { environment } from '../../environments/environments';
@Injectable({
  providedIn: 'root'
})
export class AudiencesService {

  constructor( public http: HttpClient) { }


  getPreviewTableData(){
    return this.http
      .get(`${environment.apiUrl}/get-dataset-sample/customers`)
      .pipe(
        catchError(this.handleError)
      );
  }

  // getPreviewTableData(){
  //   return this.http
  //     .get(`assets/audience.json`)
  //     .pipe(
  //       catchError(this.handleError)
  //     );
  // }

   getPreviewTableDataEvents(){
    return this.http
      .get(`${environment.apiUrl}/get-dataset-sample/events`)
      .pipe(
         catchError(this.handleError)
       );
   }

  //  getPreviewTableDataEvents(){
  //   return this.http
  //     .get(`assets/events.json`)
  //     .pipe(
  //        catchError(this.handleError)
  //      );
  //  }

  //  getPreviewTableDataTransactions(){
  //   return this.http
  //     .get(`assets/transactions.json`)
  //     .pipe(
  //        catchError(this.handleError)
  //      );
  //  }

  getPreviewTableDataTransactions(){
    return this.http
      .get(`${environment.apiUrl}/get-dataset-sample/transactions`)
      .pipe(
         catchError(this.handleError)
       );
   }
  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {

      console.error('An error occurred:', error.error);
    } else {
    }
    return throwError(
      'Something bad happened; please try again later.');
  }

  generateQuery(question: any) {
    const head = new HttpHeaders().set('content-type', 'application/json')
    let options = {
      headers: head
    }
    // let questionData = {
    //   "question": query
    // }
    return this.http.post(`${environment.apiUrl}/post-audiences`, {question}, options)
      .pipe(catchError(this.handleError));

  }

  getaudienceTableData(){
    return this.http
      .get(`assets/audienceEmailDetails.json`)
      .pipe(
         catchError(this.handleError)
       );
   }



  updateCampaign(query: any, userId: string , campaignId: string) {
    const head = new HttpHeaders().set('content-type', 'application/json')
    let options = {
      headers: head
    }
    return this.http.put(`${environment.apiUrl}/users/${userId}/campaigns/${campaignId}`, query, options)
      .pipe(catchError(this.handleError));

  }
}
