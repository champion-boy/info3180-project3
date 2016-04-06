
'use strict';

(function(angular) {
	
	angular
		.module('wishlist')
		.controller('HomeCtrl', 
			['$log', homeCtrl]);
		
	function homeCtrl($log) {
		$log.log("HomeCtrl");
	}

})(angular);