'use strict';

(function(angular) {

	angular
		.module('wishlist')
		.controller('WishlistShowCtrl', 
			['$scope', '$http', 'WishlistService', '$stateParams', '$log', wishlistShowCtrl]);

	function wishlistShowCtrl($scope, $http, WishlistService, $stateParams, $log) {
		var userId = $stateParams.userId,
			wishlistName = $stateParams.wishlistName;

		WishlistService.get(userId, wishlistName, 
			wishlistLoadedSuccess, wishlistLoadFail);

		function wishlistLoadedSuccess(res) {
			$log.log(res.data);
			var wishlist = res.data.wishlsit;
			$scope.wishlist = wishlist;
			$http.get('/api/users/' + userId + '/wishlists/' + wishlistName + '/items')
				.then(itemsLoadSuccess, itemsLoadFail);
		}

		function itemsLoadSuccess(res) {
			var items = res.data.items;
			$scope.items = items;
		}

		function itemsLoadFail(res) {
			$log.log('Failed to load wishlist items');
		}
		
		function wishlistLoadFail(res) {
			$log.log("Failed to load wishlist");
		}
	}

})(angular);