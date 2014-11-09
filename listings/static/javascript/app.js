'use strict';

var app = angular.module('app', ['ui.router', 'restangular']);

// http://localhost:8000/api/listing/?offset=0&limit=20&format=json
// http://localhost:8000/api/listing/?offset=20&limit=20&format=json