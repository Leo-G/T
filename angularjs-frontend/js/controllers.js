angular.module('myApp.controllers', []).controller('UserListController', function($scope, $state,  User, $auth) {


 var columnDefs = [ {headerName: "Sr No", width: 50, cellRenderer: function(params) {
            return params.node.id + 1;
            }}, 
    {
    headerName: "email",
    field: "email",
    width: 300
  }, {
    headerName: "name",
    field: "name",
    width: 500
  }, {
    headerName: "is_active",
    field: "is_active"
  },
                  
    {
    headerName: "role",
    field: "role"
  }];


  $scope.gridOptions = {
    columnDefs: columnDefs,
    rowData: null,
    enableSorting: true,
    enableColResize: true,
    rowSelection: 'single',

  };
  
  User.get(function(data) {
    $scope.users = data.data[0].attributes ;
    $scope.gridOptions.rowData = $scope.users;
    $scope.gridOptions.api.onNewRows();
    $scope.gridOptions.api.sizeColumnsToFit();
  }, function(error){
      $scope.error = error.data;
  });
  
}).controller('UserAddController', function($scope, $state, $stateParams, User, $window) {
  $scope.user = new User();  //create new site instance. Properties will be set via ng-model on UI

  $scope.addUser = function() { //create a new site. Issues a POST to /api/sites
    $scope.user.$save(function() {
      $window.alert("User Saved");
      $state.go('users'); // on success go back to home i.e. sites state.
    }, function(error) {
    $window.alert(error.data);
    } );
  };
}).controller('LoginController', function($auth, $state, $window, $scope, toaster) {	
	
	 $scope.login = function() {
            $scope.credentials = {
                
                  "data": {
                    "type": "users",
                    "attributes": {                     
                      "email": $scope.email,
                      "password": $scope.password,
                    

                      }
                     }
                  }
            
            
            
            // Use Satellizer's $auth.login method to verify the username and password
            $auth.login($scope.credentials).then(function(data) {

                // If login is successful, redirect to users list
               
				$state.go('users');
            })
            .catch(function(response){ // If login is unsuccessful, display relevant error message.
               
               
               toaster.pop({
                type: 'error',
                title: 'Login Error',
                body: response.data,
                showCloseButton: true,
                timeout: 0
                });
               });
        }
		
        
 
}).controller('LogoutCtrl', function($auth,  $location, toaster) { // Logout the user if they are authenticated.
	
	
	if (!$auth.isAuthenticated()) { return; }
     $auth.logout()
      .then(function() {
      
        toaster.pop({
                type: 'success',               
                body: 'Logging out' ,
                showCloseButton: true,
                
                });
        $location.url('/');
      }); 
		
        
 
}).controller('NavCtrl', function($auth,  $scope) {
	
	//Display the Logout button for authenticated users only
	$scope.isAuthenticated = function() {
      return $auth.isAuthenticated();
    };
		
        
 
});



  