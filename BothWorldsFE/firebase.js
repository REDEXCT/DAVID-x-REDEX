// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAk3CIOsLoTtxOPexmcmZBxxHvYkSWNs90",
  authDomain: "bothworlds-b48d2.firebaseapp.com",
  projectId: "bothworlds-b48d2",
  storageBucket: "bothworlds-b48d2.appspot.com",
  messagingSenderId: "263295400018",
  appId: "1:263295400018:web:9dc85099025519eb93078b",
  measurementId: "G-GNYSS219C2"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);