'use strict';

angular.module('melinder')

    .controller('categoryController', function($scope,productsService,Session,$state ){

        $scope.categories = [];

        productsService.getCategories(function(data){
            $scope.categories = data.data._items;
        });


        $scope.guardarCategories=function(categories){
            var catPost = [];
            console.log( $scope.categories.length ? true : false);
            for(var i = 0; i < $scope.categories.length; i++ ){
                if($scope.categories[i].checked){
                    catPost.push($scope.categories[i]._id);
                }
            }
            productsService.saveCategories(Session.id || window.user.id, catPost,function(data){
                $state.go('user.menu');
            });

        }

    });