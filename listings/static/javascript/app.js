'use strict';

// before deploy to heroku, I'll have to deal with deploying JS to cdn or use
// python manage.py runserver --insecure
// https://docs.djangoproject.com/en/1.7/howto/static-files/deployment/#serving-static-files-from-a-cloud-service-or-cdn

var app = angular.module('app', ['ui.router', 'ui.bootstrap', 'angular-data.DS']);

angular.module('app').config(function ($stateProvider, $urlRouterProvider, $locationProvider) {

    $locationProvider.html5Mode(true).hashPrefix('');

    // For any unmatched url, send to /route1
    $urlRouterProvider.otherwise("/buy/all/1");
    $stateProvider
        .state('listingList', {
            url: "/:buyOrSell/:category/:page",
            templateUrl: "/static/html/partials/_listing_list.html",
            controller: "ListingListController"
        })
        .state('listing', {
            url: "/listing/:id",
            templateUrl: "/static/html/partials/_listing.html",
            controller: "ListingController"
        });
});

angular.module('app').run(['DS', 'DSHttpAdapter', function(DS, DSHttpAdapter) {
  DSHttpAdapter.defaults.forceTrailingSlash = true;
}]);

// http://stackoverflow.com/questions/23585065/angularjs-ui-router-change-url-without-reloading-state
angular.module('app').config(['$urlRouterProvider', function ($urlRouterProvider) {
    $urlRouterProvider.deferIntercept();
}]);
angular.module('app').run(['$rootScope', '$urlRouter', '$location', '$state', '$window', function ($rootScope, $urlRouter, $location, $state, $window) {
    $rootScope.$on('$locationChangeSuccess', function(e, newUrl, oldUrl) {
      e.preventDefault(); // Prevent $urlRouter's default handler from firing

      // http://www.arnaldocapo.com/blog/post/google-analytics-and-angularjs-with-ui-router/72
      if (!$window.ga) return;
      $window.ga('send', 'pageview', { page: $location.path() });

      // if going from ListingList to ListingList, don't refresh!
      var isListingListController = $state.current.name === 'listingList';
      var goingToListingListController= newUrl.indexOf("/buy/") > -1 || newUrl.indexOf("/sell/") > -1;

      // console.log("newUrl: " + newUrl);
      // console.log("oldUrl: " + oldUrl);
      // console.log("isListingListController: " + isListingListController);
      // console.log("goingToListingListController: " + isListingListController);

      if (!(isListingListController && goingToListingListController)) { $urlRouter.sync(); };

    });
    $urlRouter.listen();
}]);

app.factory('Listing', ['DS', '$rootScope', function (DS, $rootScope) {
  return DS.defineResource({
    name: 'listing',
    baseUrl: '/api/v1',
    deserialize: function(name, data) {
      $rootScope.listingLastMeta = data.data.meta;
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

app.factory('Seller', ['DS', '$rootScope', function (DS, $rootScope) {
  return DS.defineResource({
    name: 'seller',
    baseUrl: '/api/v1',
    deserialize: function(name, data) {
      $rootScope.sellerLastMeta = data.data.meta;
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

angular.module('app').controller('ListingListController', ['$scope', '$window', '$state', '$location', '$anchorScroll', '$stateParams', '$modal', '$rootScope', '$timeout', 'Listing', 'Seller', function($scope, $window, $state, $location, $anchorScroll, $stateParams, $modal, $rootScope, $timeout, Listing, Seller) {
  $scope.listingsMeta = {};
  $scope.listingsMeta.total_count = 10000; // initialize to a large number so $stateParams.page does not get overwritten
  $scope.$location = $location;
  $scope.$stateParams = $stateParams;
  $scope.numPerPage = 10;
  $scope.filters = {
    buy_or_sell: $stateParams.buyOrSell,
    category: $stateParams.category,
    message__contains: ""
  };
  $scope.categories = ['all', 'textbook', 'tickets', 'bedding', 'instrument', 'personal', 'food', 'household', 'clothing', 'furniture', 'kitchen', 'trash', 'tech', 'sublet', 'longboard', 'gaming', 'sports', 'tools', 'cars', 'holiday'];
  $scope.updateURL = function () { $location.url($scope.filters.buy_or_sell + "/" + $scope.filters.category + "/" + $stateParams.page); }
  function scrollToTop() { var old = $location.hash(); $location.hash('top'); $anchorScroll(); $location.hash(old); }
  function getListings() {
    var params = angular.copy($scope.filters);
    if (params.category == "all") {  delete params.category; }
    params.offset = ($stateParams.page - 1) * $scope.numPerPage;
    params.limit = $scope.numPerPage;
    params.order_by="-updated_time";
    Listing.findAll(params, { bypassCache: true }).then(function(data) { 
      $scope.listings = data; // (hopefully) temporary, see: https://github.com/jmdobry/angular-data/issues/236#issuecomment-62346279
      $scope.listingsMeta = $rootScope.listingLastMeta;
    });
  }
  getListings();

  $scope.$watch('[filters, $stateParams.page]', function(newVal, oldVal){ 
    if (newVal === oldVal) {return;} 
    if (oldVal[1] == newVal[1]) { $stateParams.page = 1; }
    getListings(); 
  }, true);
  $scope.$watch("listings", function (value) { var val = value || null; if (val) scrollToTop(); });

  $scope.open = function (size) {
    var modalInstance = $modal.open({
      templateUrl: '/static/html/partials/_about_modal.html',
      controller: 'ModalInstanceCtrl',
      size: size,
    });
  };

  $window.Listing = Listing;
  $window.$scope1 = $scope;
}]);

angular.module('app').controller('ModalInstanceCtrl', function ($scope, $modalInstance) {
  $scope.ok = function () { $modalInstance.close(); };
  $scope.cancel = function () { $modalInstance.dismiss('cancel'); };
});

angular.module('app').controller('ListingController', ['$scope', '$window', '$location', '$anchorScroll', '$stateParams', '$modal', 'Listing', 'Seller', function($scope, $window, $location, $anchorScroll, $stateParams, $modal, Listing, Seller) {
  Listing.find($stateParams.id).then(function(data) { $scope.listing = data; });
  $window.$scope2 = $scope;
}]);


// http://localhost:8000/api/v1/listing/?offset=0&limit=20&format=json
// http://localhost:8000/api/v1/listing/?offset=20&limit=20&format=json
