'use strict';

(function(angular) {

	angular
		.module('wishlist')
		.controller('RegisterCtrl', 
			['Session', 'UserService', '$state', '$http', '$log', '$scope', 
			'localStorageService', 
				registerCtrl]);

	function registerCtrl(Session, UserService, $state, $http, $log, $scope, 
		localStorageService) {
		
		$scope.user = {};
		

		$scope.createUser = function(user) {
			UserService.register(user, registerSuccess, registerFail);

			function registerSuccess(response) {
				$log.log('RegisterCtrlefe');
				$log.log(response.data);

				var data = response.data;
				Session.save(data);
				$state.go('users_show', {'userId': data.user_id});
			}

			function registerFail(response) {
				$log.log('RegisterCtrlefefefefef');
				$log.log(response);
			}

		};
	}

})(angular);