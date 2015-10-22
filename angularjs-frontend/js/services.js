angular.module('myApp.services', []).factory('User', function($resource) {
  return $resource('api/v1/users/:id', { id:'@user.id' }, {
    update: {
      method: 'PATCH',
      
     
     
    }
    }, {
    stripTrailingSlashes: false
    });
});