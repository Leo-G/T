angular.module('myApp', ['ui.router', 'ngResource', 'myApp.controllers', 'myApp.services', "angularGrid" , 'satellizer','toaster', 'ngAnimate']);

angular.module('myApp').config(function($stateProvider, $urlRouterProvider, $authProvider) {
	
	  // Satellizer configuration that specifies which API
            // route the JWT should be retrieved from
            $authProvider.loginUrl = '/api/v1/login/';

            
            $urlRouterProvider.otherwise('/');
            
  $stateProvider. state('login', {
	url: '/login',
	templateUrl: 'partials/login.html',
	controller: 'LoginController',
    resolve: {
          skipIfLoggedIn: skipIfLoggedIn
        }
     
  }).state('users', { // state for showing all users
    url: '/',
    templateUrl: 'partials/users.html',
    controller: 'UserListController',
    resolve: { //resolve only for authenticated users
          loginRequired: loginRequired
        }
  }).state('viewSite', { //state for showing single user
    url: '/users/:id/view',
    templateUrl: 'users-new/partials/user-view.html',
    controller: 'SiteViewController',
    resolve: {
          loginRequired: loginRequired
        }
  }).state('newUser', { //state for adding a new user 
    url: '/users/new',
    templateUrl: '/users/add_user.html',
    controller: 'UserCreateController',
    resolve: {
          loginRequired: loginRequired
        }
  }).state('editSite', { //state for updating a user
    url: '/users/:id/edit',
    templateUrl: 'users-new/partials/user-edit.html',
    controller: 'SiteEditController',
    resolve: {
          loginRequired: loginRequired
        }
  }).state('logout', {
        url: '/logout',
        template: null,
        controller: 'LogoutCtrl'
      });
      
   
  //If a user is already logged in, the Login window if requested need not be displayed.
   function skipIfLoggedIn($q, $auth) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
       
       
        deferred.reject();
        
      } else {
        deferred.resolve();
      }
      return deferred.promise;
    }
    
   //Redirect unauthenticated users to the login state
   function loginRequired($q, $location, $auth, $state) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
        deferred.resolve();
      } else {
        $location.path('/login');
      }
      return deferred.promise;
    }
    
    
});

               