'use strict';

(function(angular) {

	angular
		.module('wishlist')
		.controller('UserAllCtrl', 
			['UserService', '$log', '$scope', userAllCtrl]);

	function userAllCtrl(UserService, $log, $scope) {
		$log.log("In UserAllCtrl");

		UserService.all(usersLoaded, failedToLoadUsers);

		function usersLoaded(res) {
			$log.log(res.data);
			$scope.users = res.data.users;
		}

		function failedToLoadUsers(res) {
			$log.log('Failed to load users');
		}
	}

})(angular);