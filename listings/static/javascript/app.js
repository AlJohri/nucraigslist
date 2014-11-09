'use strict';

// before deploy to heroku, I'll have to deal with deploying JS to cdn or use
// python manage.py runserver --insecure
// https://docs.djangoproject.com/en/1.7/howto/static-files/deployment/#serving-static-files-from-a-cloud-service-or-cdn

var app = angular.module('app', ['ui.router', 'angular-data.DS']);

angular.module('app').config(function ($stateProvider, $urlRouterProvider) {
    // For any unmatched url, send to /route1
    $urlRouterProvider.otherwise("/");
    $stateProvider
        .state('index', {
            url: "/",
            templateUrl: "/static/html/partials/_listing_list.html",
            controller: "HomeController"
        });
});

angular.module('app').run(['DS', 'DSHttpAdapter', function(DS, DSHttpAdapter) {
	DSHttpAdapter.defaults.forceTrailingSlash = true;
}]);


app.factory('Listing', ['DS', function (DS) {
  return DS.defineResource({ 
  	name: 'listing', 
  	baseUrl: '/api/v1',
  	deserialize: function(name, data) { 
  		Listing.meta = data.data.meta;
  		return data.data.objects;
  	},
    relations: {
      // belongsTo: {
      //   seller: {
      //     parent: true,
      //     localKey: 'seller',
      //     localField: 'seller'
      //   }
      // }
    }
  });
}]);

app.factory('Seller', ['DS', function (DS) {
  return DS.defineResource({ 
    name: 'seller', 
    baseUrl: 'api/v1',
    deserialize: function(name, data) { 
      Seller.meta = data.data.meta;
      return data.data.objects;
    }
  });
}]);

angular.module('app').controller('HomeController', ['$scope', '$window', 'Listing', function($scope, $window, Listing) {

	Listing.findAll({limit: 100}).then(function(){
		$scope.meta = Listing.meta;
	});
	Listing.bindAll($scope, 'listings', {});

	$window.Listing = Listing;
}]);


// http://localhost:8000/api/v1/listing/?offset=0&limit=20&format=json
// http://localhost:8000/api/v1/listing/?offset=20&limit=20&format=json