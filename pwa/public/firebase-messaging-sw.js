importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-messaging.js');

// Initialize the Firebase app in the service worker by passing in the
// messagingSenderId.
firebase.initializeApp({
   'messagingSenderId': '272062630249',
   'apiKey': 'AAAAP1gySWk:APA91bEJogPOykWMPEc4hoFer2QXo0uOijVODd2AHrb0qHsIWFRLAFGEDw-YZfEVi0oC9G_zh2j2dZ4RIvMyJi-cf3kvo2gZMRHN8PFvYDMwzAFVk4qlLmo5NyQNXhZNvzlqP7w6pG20',
   'projectId': 's8project-test', 
   'appId': '1:272062630249:web:5dd41ef42e40ce579095f8',
});

// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Customize notification here
  const notificationTitle = 'Background Message Title';
  const notificationOptions = {
    body: 'Background Message body.',
    icon: '/itwonders-web-logo.png'
  };

  return self.registration.showNotification(notificationTitle,
      notificationOptions);
});