'use strict';

(function(angular){
	angular
		.module('wishlist', [
			'ngMaterial', 'ui.router', 'LocalStorageModule',
			'ngResource'
		])
		.config(['$stateProvider', '$urlRouterProvider', 
		'localStorageServiceProvider', '$httpProvider', 
			initConfig])
		.run(['$log', '$state', '$rootScope', 'Session', initRun]);

	function initRun($log, $state, $rootScope, Session) {
		$rootScope.$on('$stateChangeStart', function(event, toState) {
			if (toState.data != undefined && !angular.isFunction(toState.data.auth)) 
				return;
			
			// var isAuthenticated = toState.data.auth(Session.getToken);

			// if (!isAuthenticated) {
			// 	event.preventDefault();
			// 	$state.go('home', {notify: false});
			// }
		});
	}

	function initConfig($stateProvider, $urlRouterProvider, localStorageServiceProvider,
		$httpProvider) {

		localStorageServiceProvider.setNotify(true, true);

		$urlRouterProvider.otherwise('/');

		$stateProvider
			.state('home', {
				url: '/',
				templateUrl: templatePath('pages/home'),
				controller: 'HomeCtrl'
			})
			.state('login', {
				url: '/login',
				templateUrl: templatePath('sessions/login'),
				controller: 'LoginCtrl'
			})
			.state('register', {
				url: '/register',
				templateUrl: templatePath('sessions/register'),
				controller: 'RegisterCtrl'
			})
			.state('logout', {
				url: '/logout',
				controller: 'LogoutCtrl'
			})
			.state('users_all', {
				url: '/users',
				templateUrl: templatePath('users/all'),
				controller: 'UserAllCtrl'
			})
			.state('users_show', {
				url: '/users/:userId',
				templateUrl: templatePath('users/show'),
				controller: 'UserShowCtrl'
			})
			.state('wishlists_new', {
				url: '/wishlists/new',
				templateUrl: templatePath('wishlists/new'),
				controller: 'WishlistNewCtrl',
				data: {
					auth: function(auth) {
						return auth.token.length > 0;
					}
				}
			})
			.state('wishlists_all', {
				url: '/users/{userId}/wishlists',
				templateUrl: templatePath('wishlists/all'),
				controller: 'WishlistAllCtrl'
			})
			.state('wishlists_show', {
				url: '/users/{userId}/wishlists/{wishlistName}',
				templateUrl: templatePath('wishlists/show'),
				controller: 'WishlistShowCtrl'
			})
			.state('items_new', {
				url: '/users/{userId}/wishlists/{wishlistId}/items/new',
				templateUrl: templatePath('items/new'),
				controller: 'ItemNewCtrl'
			})
			.state('items_all', {
				url: '/users/{userId}/wishlists/{wishlistId}/items',
				templateUrl: templatePath('items/all'),
				controller: 'ItemAllCtrl'
			})
			.state('items_show', {
				url: '/users/{userId}/wishlists/{wishlistName}/items/{itemNo}',
				templateUrl: templatePath('items/show'),
				controller: 'ItemShowCtrl'
			});

		function templatePath(path) {
			return 'partials/' + path + '.html';
		}
	}

})(angular);