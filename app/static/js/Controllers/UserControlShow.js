
'use strict';
		
(function(angular) {

	angular
		.module('wishlist')
		.controller('UserShowCtrl',
			['$state', 'UserService', '$log', '$stateParams', '$scope', '$http', 
			'Session', userShowCtrl]);
		
	function userShowCtrl($state, UserService, $log, $stateParams, $scope, $http,
		Session) {

		var id = $stateParams.userId;
		$scope.user = {}

		UserService.get(id, userDetailsLoaded, userLoadFailed);

		$scope.createNewWishlist = function() {
			$state.go('wishlists_new');
		}

		function userDetailsLoaded(res) {
			$scope.user = res.data.user;
		}
		
		function userLoadFailed(res) {
			$log.log("Failed to load user");
		}
	}

})(angular);