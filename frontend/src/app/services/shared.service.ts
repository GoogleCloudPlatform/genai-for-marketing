import { Injectable, inject } from '@angular/core';
import { LoginService } from './login.service';
import { Firestore, collection, collectionData } from '@angular/fire/firestore';
import { GoogleAuthProvider, getAuth, signInWithPopup, User } from '@firebase/auth';
import { getStorage, ref, uploadBytesResumable } from "firebase/storage";
import { initializeApp } from '@angular/fire/app';
import { Auth } from '@angular/fire/auth';
@Injectable({
  providedIn: 'root'
})
export class SharedService {
  userData: any;
  private auth: Auth = inject(Auth);
  
  constructor(private fs: Firestore, public loginservice: LoginService) { }
  fireBaseConfig = {
    apiKey: "",
    authDomain: "",
    projectId: "",
    storageBucket: "",
    messagingSenderId: "",
    appId: "",
    measurementId: ""
  };

  async googleSignin() {
    const provider = new GoogleAuthProvider();

    return await signInWithPopup(this.auth, provider)

      .then((result) => {
        return result.user
      }).
      catch(

        function(error) {
          // Handle Errors here.
          var errorCode = error.code;
          if (errorCode === 'auth/account-exists-with-different-credential') {
            alert('You have already signed up with a different auth provider for that email.');
            // If you are using multiple auth providers on your app you should handle linking
            // the user's accounts here.
          } else {
            console.error(error);
          }
        });
  }
}
