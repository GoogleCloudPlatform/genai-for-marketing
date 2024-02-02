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
    apiKey: "AIzaSyBssyJ8TV7oIy09YMFLhmj1ZwnzzxhQ4Nk",
    authDomain: "rl-llm-dev.firebaseapp.com",
    projectId: "rl-llm-dev",
    storageBucket: "rl-llm-dev.appspot.com",
    messagingSenderId: "244831775715",
    appId: "1:244831775715:web:d649215b84c64c4b97ced6",
    measurementId: "G-VG39L9XTKZ"
  };


  // async googleSignin() {
  //   const provider = new GoogleAuthProvider();

  //   // const credential = await this.afAuth.signInWithPopup(provider);
  //   // return this.updateUserData(credential.user);
  //   const app = initializeApp(this.fireBaseConfig);
  //   const auth = getAuth(app);
  //   const storage = getStorage(app);
  //   return await signInWithPopup(auth, provider)
  //     .then((result) => {
  //       return result.user
  //     }).
  //     catch(

  //       function (error) {
  //         // Handle Errors here.
  //         var errorCode = error.code;
  //         var errorMessage = error.message;
  //         var photoUrl = error.photoUrl;
  //         // The email of the user's account used.
  //         var email = error.email;
  //         // The firebase.auth.AuthCredential type that was used.
  //         var credential = error.credential;
  //         if (errorCode === 'auth/account-exists-with-different-credential') {
  //           alert('You have already signed up with a different auth provider for that email.');
  //           // If you are using multiple auth providers on your app you should handle linking
  //           // the user's accounts here.
  //         } else {
  //           console.error(error);
  //         }
  //       });
  // }
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
