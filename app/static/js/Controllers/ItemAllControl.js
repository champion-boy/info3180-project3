
'use strict';

(function(angular) {

	angular
		.module('wishlist')
		.controller('ItemAllCtrl', 
			['$scope', '$stateParms', '$state', '$log', itemAllCtrl]);

	function itemAllCtrl($scope, $stateParams, $state, $log) {
		var userId = $stateParams.userId,
			wishlistName = $stateParams.wishlistName,
			itemNo = $stateParams.itemNo;

		$scope.goToNewItemForm = function() {
			$state.go('items_new', {
				userId: userId,
				wishlistName: wishlistName,
				itemNo: itemNo
			});
		};
	}

})(angular);