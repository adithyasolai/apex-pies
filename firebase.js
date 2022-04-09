// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDgRXCVekaokY7o_D1ZAxK8smCXj3CqqIQ",
  authDomain: "apex-pies.firebaseapp.com",
  databaseURL: "https://apex-pies-default-rtdb.firebaseio.com",
  projectId: "apex-pies",
  storageBucket: "apex-pies.appspot.com",
  messagingSenderId: "744272199796",
  appId: "1:744272199796:web:72557435a41d6f85489121",
  measurementId: "G-Z3ZW9870KS"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);