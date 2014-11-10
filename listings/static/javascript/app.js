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
      Listing.lastMeta = data.data.meta;
      if (data.data.objects !== undefined) {
        return data.data.objects;
      } else {
        return data.data;
      }
    },
    relations: {
      belongsTo: {
        seller: {
          localField: 'seller',
          localKey: 'sellerId'
        }
      }
    }
  });
}]);

app.factory('Seller', ['DS', function (DS) {
  return DS.defineResource({
    name: 'seller',
    baseUrl: '/api/v1',
    deserialize: function(name, data) {
      // debugger;
      if (data.data.objects !== "undefined") {
        return data.data.objects;
      } else {
        return data.data;
      }
    },
    relations: {
      hasMany: {
        listing: {
          localField: 'listings',
          foreignKey: 'sellerId'
        }
      },
    }
  });
}]);


angular.module('app').controller('HomeController', ['$scope', '$window', 'Listing', 'Seller', function($scope, $window, Listing, Seller) {

  Listing.findAll({limit: 100}).then(function(data) { $scope.lastMeta = Listing.lastMeta; } );
  Seller.findAll();
  Listing.bindAll($scope, 'listings', {});
  Seller.bindAll($scope, 'sellers', {});

  console.log(Listing.filter({limit: 1})[0]);
  $scope.bs = "buy";
  $window.Listing = Listing;
  $window.Seller = Seller;
  $window.$scope = $scope;

}]);


// http://localhost:8000/api/v1/listing/?offset=0&limit=20&format=json
// http://localhost:8000/api/v1/listing/?offset=20&limit=20&format=json
