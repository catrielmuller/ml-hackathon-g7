'use strict';

angular.module('melinder')
    .factory('productsService', function($http){

        var procuctsService = {
            getCategories:function(callback){
                $http.get(API_DOMAIN+'/api/category').then(callback);
            },
            getProductsByCategory:function(categoryId,callback){
                $http.get(API_DOMAIN+' /api/product?where={"category": "'+categoryId+'"}').then(callback);
            },
            voteProduct:function(productId,vote,callback){
                $http.post(API_DOMAIN+' /api/product/'+productId+'/like ',vote).then(callback);
            },
            saveCategories:function(userId,categories,callback){
                $http.post(API_DOMAIN+' /api/user/'+userId,{preferences:categories}).then(callback);
            }
        };

        return procuctsService;
    });