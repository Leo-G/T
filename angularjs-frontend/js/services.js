angular.module('myApp.services', []).factory('Api', function($resource) {
  return{User: $resource('api/v1/users/:id', { id:'@user.id' }, {
    update: {
      method: 'PATCH',
      
     
     
    }
    }, {
    stripTrailingSlashes: false
    }),
   Role: $resource('api/v1/roles/:id', { id:'@role.id' }, {
    update: {
      method: 'PATCH',
      
     
     
    }
    }, {
    stripTrailingSlashes: false
    })
 }
});

