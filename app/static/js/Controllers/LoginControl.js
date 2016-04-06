
'use strict';

(function(angular) {
	
	angular
		.module('wishlist')
		.controller('LoginCtrl', 
			['Session', 'UserService', 'localStorageService', '$scope', '$log', loginCtrl]);

	function loginCtrl(Session, UserService, localStorageService, $scope, $log) {
		$scope.credentials = {};

		$scope.authenticate = function(credentials) {
			UserService.login(credentials, loginSuccessful, loginFailure);

			function loginSuccessful(res) {
				var data = response.data;
				Session.save(data);
				$state.go('user_show', {'userId': data.user_id});
			}

			function loginFailure(res) {
				$log.log(res);
			}
		}
	}

})(angular);