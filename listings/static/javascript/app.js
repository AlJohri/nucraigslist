'use strict';

var app = angular.module('app', ['ui.router', 'ngResource']);

app.config(function ($stateProvider, $urlRouterProvider) {
    // For any unmatched url, send to /route1
    $urlRouterProvider.otherwise("/");
    $stateProvider
        .state('index', {
            url: "/",
            templateUrl: "/static/html/partials/_listing_list.html",
            controller: "HomeController"
        });
});

angular.module('app').controller('HomeController', ['$scope', '$resource', '$http', function($scope, $resource, $http) {

	console.log("shit");

	var Listing = $resource('/api/v1/listing/', {}, {
	    query: {
	        method: 'GET',
	        isArray: true,
	        transformResponse: $http.defaults.transformResponse.concat([
	            function (data, headersGetter) {
	            	console.log(data.objects);
	                return data.objects;
	            }
	        ])
	    }
	});

	Listing.query(function(data) {
		$scope.listings = data;
	});

}]);


// http://localhost:8000/api/v1/listing/?offset=0&limit=20&format=json
// http://localhost:8000/api/v1/listing/?offset=20&limit=20&format=json