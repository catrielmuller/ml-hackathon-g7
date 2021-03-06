'use strict';

angular.module('melinder').service('Session', function () {

    this.create = function (userId,username,email,preferences) {
        this.id = userId;
        this.username =username;
        this.email = email;
        this.preferences = preferences;

        window.user = this;
    };


    this.destroy = function () {
        this.id = null;
        this.username =null;
        this.email = null;
        this.preferences = null;
    };

    this.isAlive = function(){
        return this.id && this.username && this.email && this.preferences;
    }

})

angular.module('melinder')
    .factory('userService', function($http,Session){

        var userService = {
            logout:function(){
                Session.destroy();
            },
            getUserLoggued:function(callback){

                if(!Session.isAlive()){
                    $http.get(API_DOMAIN +'/api/me').then(function(dataUser){
                            Session.create(dataUser.data.id,dataUser.data.userName,dataUser.data.email,dataUser.data.preferences);

                        if(callback) callback(dataUser.data);
                    });
                }else{
                    return Session;
                }
        },

            setPreferences:function(preferences,callback){
                if(Session.isAlive()){
                    $http.post('/api/user/'+Session.id,preferences).then(callback || function(){});
                }
            }
        };

        return userService;
    });




