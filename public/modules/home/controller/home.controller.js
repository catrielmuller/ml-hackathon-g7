'use strict';

var module = angular.module('home' , []);

module.controller('homeController', ['$scope'], function($scope){
    $scope.test = 'MiVariable';
});