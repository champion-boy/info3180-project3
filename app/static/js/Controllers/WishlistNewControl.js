'use strict';

(function(angular) {
	
	angular
		.module('wishlist')
		.controller('WishlistNewCtrl', 
			['$state', 'Session', 'WishlistService', '$scope', '$log', wishlistNewCtrl]);

	function wishlistNewCtrl($state, Session, WishlistService, $scope, $log) {
		$scope.wishlist = {};

		var token = Session.getToken(),
			user = Session.getUser();		

		if (null == token.token || null == user.userId) {
			$state.go('home');
		}

		$scope.saveWishlist = function(wishlist) {
			$log.log(wishlist);
			var config = {
				'userId': user.userId,
				'token': token.token
			};

			WishlistService.create(config, wishlist,
				wishlistSavedSuccess, wishlistSaveFail)
		}

		function wishlistSavedSuccess(res) {
			$log.log(res.data);
			if (res.data.error != undefined) {
				$scope.error = res.data.error;
				return 
			}

			$state.go('wishlists_all', {userId: user.userId});
		}

		function wishlistSaveFail(res) {
			$log.log('Failed to save wishlist');
		}
	}

})(angular);