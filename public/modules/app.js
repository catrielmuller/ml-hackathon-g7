'use strict';


var lib = [],
    venderLibs = ['ui.router'],
    modules = ['home'];

lib.concat(venderLibs,modules)

var app = angular.module('melinder', lib);
