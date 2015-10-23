angular.module('myApp', ['ui.router', 'ngResource', 'myApp.controllers', 'myApp.services', "angularGrid" , 'satellizer','toaster', 'ngAnimate']);

angular.module('myApp').config(function($stateProvider, $urlRouterProvider, $authProvider) {
	
	  // Satellizer configuration that specifies which API
            // route the JWT should be retrieved from
            $authProvider.loginUrl = '/api/v1/login/';

            
            $urlRouterProvider.otherwise('/login');
            
  $stateProvider.state('login', {
	url: '/login',
	templateUrl: 'partials/login.html',
	controller: 'LoginController',
    resolve: {
          skipIfLoggedIn: skipIfLoggedIn
        }
     
  }).state('admin', {
	url: '/admin',
	templateUrl: 'admin/index.html',
	//controller: 'LoginController',
    resolve: {
          loginRequired: loginRequired
        }
     
  }).state('users', { // state for showing all users
    url: '/users',
    templateUrl: 'users/index.html',
    controller: 'UserListController',
    resolve: { //resolve only for authenticated users
          loginRequired: loginRequired
        }
  
  }).state('newUser', { //state for adding a new user 
    url: '/users/new',
    templateUrl: '/users/add_user.html',
    controller: 'UserCreateController',
    resolve: {
          loginRequired: loginRequired
        }
  }).state('editUser', { //state for updating a user
    url: '/users/:id/edit',
    templateUrl: 'users/edit_user.html',
    controller: 'UserEditController',
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

               