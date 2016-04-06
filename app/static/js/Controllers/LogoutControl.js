'use strict';

(function(angular) {
	angular
		.module('wishlist')
		.controller('LogoutCtrl', ['Session', 'UserService', '$state', '$log', logoutCtrl]);

	function logoutCtrl(Session, UserService, $state, $log) {
		UserService.logout();
		Session.clear();
		$state.go('home');
	}
})(angular);