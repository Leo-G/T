angular.module('myApp.services', []).factory('User', function($resource) {
  return $resource('api/v1/users/', {  }, {
    update: {
      method: 'PATCH',
      
     
     
    }
    }, {
    stripTrailingSlashes: false
    });
});