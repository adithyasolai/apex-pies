import { getDatabase, ref, set } from "firebase/database";
import { getStorage, ref } from "firebase/storage";

const db = getDatabase();

// Create a reference with an initial file path and name
const storage = getStorage();
const pathReference = ref(storage, '/stocks.csv');

function writeUserData(csvDict) {


    
  set(ref(db, 'tech-stocks/'), {
    username: name,
    email: email,
    profile_picture : imageUrl
  });
}