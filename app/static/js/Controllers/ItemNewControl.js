'use strict';

(function(angular) {
	
	angular
		.module('wishlist')
		.controller('ItemNewCtrl', ['$state', '$stateParams', '$scope', 'Session', 'ItemService', '$log', itemNewCtrl]);

	function itemNewCtrl($state, $stateParams, $scope, Session, ItemService, $log){
		var user = Session.getUser(),
			auth = Session.getToken(),
			wishlistId = $stateParams.wishlistId;

		$scope.saveItem = function(item) {
			var config = {
				'token': auth.token
			}

			item['user_id'] = user.userId;
			item['wishlist_id'] = wishlistId;
			
			ItemService.saveItem(config, item, itemSavedSuccess, itemSaveFailed)
		}

		function itemSavedSuccess(response) {
			var data = response.data;

			$state.go('wishlists_show', {
				userId: user.userId,
				wishlistId: wishlistId
			});
		}

		function itemSaveFail(response) {
			$log.error("failed to save");
		}
	}
})(angular);