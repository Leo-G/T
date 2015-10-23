angular.module('myApp.services', []).factory('User', function($resource) {
  return $resource('api/v1/users/:id', { id:'@user.id' }, {
    update: {
      method: 'PATCH',
      
     
     
    }
    }, {
    stripTrailingSlashes: false
    });
});


angular.module('myApp.services', []).factory('Role', function($resource) {
  return $resource('api/v1/roles/:id', { id:'@role.id' }, {
    update: {
      method: 'PATCH',
      
     
     
    }
    }, {
    stripTrailingSlashes: false
    });
});