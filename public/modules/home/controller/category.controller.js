'use strict';

angular.module('melinder')

    .controller('categoryController', function($scope,productsService,Session,$state ){

        $scope.categories = [];

        productsService.getCategories(function(data){
            $scope.categories = data.data._items;
        });


        $scope.guardarCategories=function(categories){
            productsService.saveCategories(Session.id,categories,function(data){
                $state.go('user.menu');
            });

        }

    });