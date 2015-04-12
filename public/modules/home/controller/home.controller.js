'use strict';

angular.module('melinder')

    .controller('homeController', function($scope ){

        $scope.products = [
            { image: 'https://pbs.twimg.com/profile_images/546942133496995840/k7JAxvgq.jpeg', name: 'asdasd fdg df hg gfh gfh gf h hjjhj' },
            { image: 'https://pbs.twimg.com/profile_images/514549811765211136/9SgAuHeY.png', name: 'asdasd fdg df hg gfh gfh gf h hjjhj' },
            { image: 'https://pbs.twimg.com/profile_images/491995398135767040/ie2Z_V6e.jpeg' , name: 'asdasd fdg df hg gfh gfh gf h hjjhj'}
        ];

        $scope.cardDestroyed = function(index) {
            $scope.products.splice(index, 1);
        };

        $scope.cardSwiped = function(index) {
            var newCard = // new card data
                $scope.products.push(newCard);
        };

        $scope.addProduct = function() {
            var newCard = cardTypes[Math.floor(Math.random() * cardTypes.length)];
            newCard.id = Math.random();
            $scope.products.unshift(angular.extend({}, newCard));
        }
    })


    .controller('CardCtrl', function($scope,TDCardDelegate ){

        $scope.onSwipeLeft = function(index) {
            console.log('LEFT SWIPE');
            $scope.addProduct();
        };
        $scope.onSwipeRight = function(index) {
            console.log('RIGHT SWIPE');
            $scope.addProduct();
        };

        $scope.onSwipeUp = function(index){
            $scope.addProduct();
            console.log('UP SWIPE');
        }

        $scope.onSwipeDown = function(index){
            console.log('DOWN SWIPE');
            $scope.addProduct();
        }

    });


