'use strict';

// before deploy to heroku, I'll have to deal with deploying JS to cdn or use
// python manage.py runserver --insecure
// https://docs.djangoproject.com/en/1.7/howto/static-files/deployment/#serving-static-files-from-a-cloud-service-or-cdn

var app = angular.module('app', ['ui.router', 'ui.bootstrap', 'angular-data.DS']);

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


angular.module('app').controller('HomeController', ['$scope', '$window', '$location', '$anchorScroll', '$modal', 'Listing', 'Seller', function($scope, $window, $location, $anchorScroll, $modal, Listing, Seller) {

  $scope.currentPage = 1;
  $scope.numPerPage = 10;

  $scope.filters = {
    buy_or_sell: "sell",
    category: 'all',
    message__contains: ""
  };

  // write a script to save the categories from csv into a js file and import the js file?
  $scope.categories = ['all', 'textbook', 'tickets', 'bedding', 'instrument', 'personal', 'food', 'household', 'clothing', 'furniture', 'kitchen', 'trash', 'tech', 'sublet', 'longboard', 'gaming', 'sports', 'tools', 'cars', 'holiday'];

  function getListings() {
    var params = angular.copy($scope.filters);
    if (params.category == "all") { 
      delete params.category;
    }
    params.offset = ($scope.currentPage - 1) * $scope.numPerPage;
    params.limit = $scope.numPerPage;
    params.order_by="-updated_time";
    Listing.findAll(params, { bypassCache: true }).then(function(data) { 
      $scope.listings = data; // (hopefully) temporary, see: https://github.com/jmdobry/angular-data/issues/236#issuecomment-62346279
      $scope.listingsMeta = Listing.lastMeta;
    });
    // Listing.bindAll($scope, 'listings', params);
  }

  getListings();  

  function scrollToTop() {
    var old = $location.hash();
    console.log(old);
    $location.hash('top');
    $anchorScroll();
    $location.hash(old);
    console.log($location.hash());
  }
  
  $scope.$watch('[filters, currentPage]', function(newVal, oldVal){
    if (newVal === oldVal) {return;}
    if (newVal[1] === oldVal[1]) { $scope.currentPage = 1; }
      // console.log('changed');
      // console.log(newVal);
    getListings();
  }, true);

  $scope.$watch("listings", function (value) {//I change here
        var val = value || null;            
        if (val)
            scrollToTop();
    });

  $scope.open = function (size) {

    var modalInstance = $modal.open({
      templateUrl: '/static/html/partials/_about_modal.html',
      controller: 'ModalInstanceCtrl',
      size: size,
    });
  };

  // Seller.findAll();
  // Seller.bindAll($scope, 'sellers', {});
  // $window.Seller = Seller;
  // console.log(Listing.filter({limit: 1})[0]);
  
  $window.Listing = Listing;
  $window.$scope = $scope;

  // $scope.$on('$viewContentLoaded', function(){
  //   console.log('here');
  //   scrollToTop();
  // });

}]);

angular.module('app').controller('ModalInstanceCtrl', function ($scope, $modalInstance) {
  $scope.ok = function () {
    $modalInstance.close();
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});


// http://localhost:8000/api/v1/listing/?offset=0&limit=20&format=json
// http://localhost:8000/api/v1/listing/?offset=20&limit=20&format=json
