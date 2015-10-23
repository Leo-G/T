angular.module('myApp.controllers', []).controller('UserListController', function($scope, $state,  User, $auth, toaster) {
 //Table header definitions  
        var columnDefs = [ {headerName: "Sr No", width: 50, cellRenderer: function(params) {return params.node.id + 1;}}, 
                            {headerName: "email", field: "email", width: 300 },
                            {headerName: "name",  field: "name",  width: 500 }, 
                            {headerName: "is_active", field: "is_active" },                                     
                            {headerName: "role",   field: "role"}
                            ];
        $scope.gridOptions = { columnDefs: columnDefs,
                               rowData: null,
                               enableSorting: true,
                               enableColResize: true,
                               rowSelection: 'single',};  
        User.get(function(data) {
                     $scope.users = [];
                     angular.forEach(data.data, function(value, key)
                                                        {
                                                       this.user = value.attributes;
                                                       this.user['id'] = value.id;
                                                       this.push(this.user);                    
                                                        },   $scope.users); 
                    $scope.gridOptions.rowData = $scope.users;
                    $scope.gridOptions.api.onNewRows();
                    $scope.gridOptions.api.sizeColumnsToFit();
                               }, 
                function(error){
                      $scope.error = error.data;
                                              });
  
  
   $scope.deleteUser = function(selected_id) { // Delete a User. Issues a DELETE to /api/users/:id
      user = User.get({ id: selected_id});
      user.$delete({ id: selected_id},function() {
        toaster.pop({
                type: 'success',
                title: 'Sucess',
                body: "User deleted successfully",
                showCloseButton: true,
                timeout: 0
                });
        $state.go('users'); //redirect to home
        $state.reload();
      }, function(error) {
         toaster.pop({
                type: 'error',
                title: 'Error',
                body: error,
                showCloseButton: true,
                timeout: 0
                });;
    });
    };
  
}).controller('UserEditController', function($scope, $state, $stateParams, toaster, $window, User) {
  $scope.updateUser = function() { //Update the edited site. Issues a PUT to /api/sites/:id
    
    $scope.user.$update({ id: $stateParams.id },function() {
     toaster.pop({
                type: 'success',
                title: 'Sucess',
                body: "Update was a success",
                showCloseButton: true,
                timeout: 0
                });
       $window.location.reload();
      //$state.go('sites'); // on success go back to home i.e. sites state.
    }, function(error) {
    toaster.pop({
                type: 'error',
                title: 'Error',
                body: error,
                showCloseButton: true,
                timeout: 0
                });
    });
  };

  
  $scope.loadUser = function() { //Issues a GET request to /api/users/:id to get a user to update
                       $scope.user = User.get({ id: $stateParams.id },
                                       function() {}, function(error) {
                                          toaster.pop({
                                                type: 'error',
                                                title: 'Error',
                                                body: error,
                                                showCloseButton: true,
                                                timeout: 0
                                                });
                                                });
                                };

  $scope.loadUser(); // Load a user 
  }).controller('UserCreateController', function($scope, $state, User, toaster Role) {
          $scope.user = new User();  //create new site instance. Properties will be set via ng-model on UI
          $scope.roles =  Role.get(function(data) {
                                     
                    function(error){
                      $scope.error = error.data;
                                              });

         $scope.addUser = function() { //create a new site. Issues a POST to /api/sites
                                $scope.user.$save(function() {
                                toaster.pop({
                                            type: 'success',
                                            title: 'Sucess',
                                            body: "User saved successfully",
                                            showCloseButton: true,
                                            timeout: 0
                                            });
                                  
                                  $state.go('users'); // on success go back to home i.e. sites state.
                                }, function(error) {
                                toaster.pop({
                                            type: 'error',
                                            title: 'Error',
                                            body: error,
                                            showCloseButton: true,
                                            timeout: 0
                                            });
                                           });
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
                // $scope.url = "http://" + $window.location.host + "/admin";
				//$location.url('/admin/');
               // $window.location.href = $scope.url;
               $state.go('admin');
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



  