// Client ID and API key from the Developer Console
var CLIENT_ID = '468077611840-i2f8nsohul2e5854i6kb39h7pjrdenu2.apps.googleusercontent.com';
var API_KEY = 'AIzaSyCzHh7Ee1D-qtoGen1DdunfwfL6NgH4kQ8';

// Array of API discovery doc URLs for APIs used by the quickstart
var DISCOVERY_DOCS = ["https://www.googleapis.com/discovery/v1/apis/people/v1/rest"];

// Authorization scopes required by the API; multiple scopes can be
// included, separated by spaces.
var SCOPES = "https://www.googleapis.com/auth/contacts.readonly";

var sortMethod = "default";

var authorizeButton = document.getElementById('authorize-button');
var signoutButton = document.getElementById('signout-button');
var createButton = document.getElementById('create-button');
var nameSortButton = document.getElementById('name-sort-button');
var genderSortButton = document.getElementById('gender-sort-button');
var birthdaySortButton = document.getElementById('birthday-sort-button');
/**
*  On load, called to load the auth2 library and API client library.
*/
function handleClientLoad() {
gapi.load('client:auth2', initClient);
}

/**
*  Initializes the API client library and sets up sign-in state
*  listeners.
*/
function initClient() {
gapi.client.init({
  apiKey: API_KEY,
  clientId: CLIENT_ID,
  discoveryDocs: DISCOVERY_DOCS,
  scope: SCOPES
}).then(function () {
  // Listen for sign-in state changes.
  gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);

  // Handle the initial sign-in state.
  updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
  authorizeButton.onclick = handleAuthClick;
  signoutButton.onclick = handleSignoutClick;
  nameSortButton.onclick = handleNameSortClick;
  genderSortButton.onclick = handleGenderSortClick;
  birthdaySortButton.onclick = handleBirthdaySortClick;

});
}

/**
*  Called when the signed in status changes, to update the UI
*  appropriately. After a sign-in, the API is called.
*/
function updateSigninStatus(isSignedIn) {
if (isSignedIn) {
  authorizeButton.style.display = 'none';
  signoutButton.style.display = 'block';
  createButton.style.display = 'block';
  nameSortButton.style.display = 'block';
  genderSortButton.style.display = 'block';
  birthdaySortButton.style.display = 'block';
  listConnectionNames();
} else {
  authorizeButton.style.display = 'block';
  signoutButton.style.display = 'none';
  createButton.style.display = 'none'
  nameSortButton.style.display = 'none';
  genderSortButton.style.display = 'none';
  birthdaySortButton.style.display = 'none';
}
}

/**
*  Sign in the user upon button click.
*/
function handleAuthClick(event) {
gapi.auth2.getAuthInstance().signIn();
}

/**
*  Sign out the user upon button click.
*/
function handleSignoutClick(event) {
gapi.auth2.getAuthInstance().signOut();
}

/**
*  Sort user based on first name.
*/
function handleNameSortClick(event) {
clearContent();
sortMethod = "name";
listConnectionNames();
}

/**
*  Sort user based on gender.
*/
function handleGenderSortClick(event) {
clearContent();
sortMethod = "gender";
listConnectionNames();
}

/**
*  Sort user based on gender.
*/
function handleBirthdaySortClick(event) {
clearContent();
sortMethod = "birthday";
listConnectionNames();
}

/**
* Append a pre element to the body containing the given message
* as its text node. Used to display the results of the API call.
*
* @param {string} message Text to be placed in pre element.
*/
function appendPre(message) {
var pre = document.getElementById('content');
var textContent = document.createTextNode(message + '\n');
pre.appendChild(textContent);
}

/**
*  Clear old content
*/
function clearContent()
{
  document.getElementById('content').innerHTML = "";
}

/**
* Print the display name if available for 10 connections.
*/
function listConnectionNames() {

gapi.client.people.people.connections.list({
   'resourceName': 'people/me',
   'pageSize': 10,
   'personFields': 'names,genders,birthdays',
 }).then(function(response) {
   var connections = response.result.connections;
   appendPre('Connections:');

   if (connections.length > 0) {
     for (i = 0; i < connections.length; i++) {

       if (typeof connections[i].names == 'undefined' ) {
         var newdata = {};
         newdata['names'] = [{"displayName": "No name found for connection."}];
         $.extend(true, connections[i], newdata);
         console.log(connections[i].genders)
         console.log(1)
       }
       if (typeof connections[i].genders == 'undefined') {
         var newdata = {};
         newdata['genders'] = [{"value": "No gender info found for connection."}];
         $.extend(true, connections[i], newdata);
         console.log(connections[i].genders)
       }
       if (typeof connections[i].birthdays == 'undefined') {
         var newdata = {};
         newdata['birthdays'] = [{"text": "No birthday info found for connection."}];
         $.extend(true, connections[i], newdata);
         console.log(connections[i].genders)
         //console.log(3)
       }
     }
   } else {
     appendPre('No upcoming events found.');
   }
   /**if (connections.length > 0) {
     for (i = 0; i < connections.length; i++) {
        nameList.push(connections[i].names[0].displayName);
        nameList.sort();
     }
     console.log(nameList)
    }**/
   if (sortMethod == "name") {
     connections.sort(function(a, b) {
     return compareStrings(a.names[0].displayName, b.names[0].displayName);
    })
   }

   if (sortMethod == "gender") {
     connections.sort(function(a, b) {
     return compareStrings(a.genders[0].value, b.genders[0].value);
    })
   }

   if (sortMethod == "birthday") {
     connections.sort(function(a, b) {
     return compareStrings(a.birthdays[0].text, b.birthdays[0].text);
    })
   }

   for (i = 0; i < connections.length; i++) {
     var person = connections[i];
     appendPre(person.names[0].displayName)
     appendPre(person.genders[0].value)
     appendPre(person.birthdays[0].text)
   }
 });
}

// Sort string alphabetically
function compareStrings(a, b) {
  // Assuming you want case-insensitive comparison
  a = a.toLowerCase();
  b = b.toLowerCase();

  return (a < b) ? -1 : (a > b) ? 1 : 0;
}