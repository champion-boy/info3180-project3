
'use strict';

(function(angular) {

	angular
		.module('wishlist')
		.controller('WishlistAllCtrl', 
			['$stateParams', '$state', '$scope', '$log', 'WishlistService', wishlistAllCtrl]);

	function wishlistAllCtrl($stateParams, $state, $scope, $log, WishlistService) {
		$scope.userId = $stateParams.userId;

		WishlistService.all($scope.userId, 
			wishlistLoadSuccess, wishlistLoadFail);

		$scope.goToWishlist = function(wishlist, event) {
			$state.go('wishlists_show', {
				'userId': $scope.userId, 
				'wishlistName': wishlist.name
			});
		}

		$scope.createWishlist = function() {
			$state.go('wishlists_new');
		}

		function wishlistLoadSuccess(response) {
			var data = response.data;
			$scope.wishlists = data.wishlists;
			$log.log($scope.wishlists);
		}

		function wishlistLoadFail(response) {
			$log.log('Fails to load wishlist');
		}
	}

})(angular);