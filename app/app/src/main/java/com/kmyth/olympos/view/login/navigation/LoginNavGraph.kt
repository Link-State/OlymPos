package com.kmyth.olympos.view.login.navigation

import androidx.compose.ui.Modifier
import androidx.navigation.NavGraphBuilder
import androidx.navigation.NavHostController
import androidx.navigation.compose.composable
import androidx.navigation.compose.navigation
import com.kmyth.olympos.LOGIN_GRAPH_ROUTE
import com.kmyth.olympos.LoginNav
import com.kmyth.olympos.composableActivityViewModel
import com.kmyth.olympos.view.login.UserLoginScreen
import com.kmyth.olympos.viewmodel.login.LoginViewModel

fun NavGraphBuilder.loginNavGraph(
    navController: NavHostController,
    modifier: Modifier
) {
    navigation(startDestination = LoginNav.route, route = LOGIN_GRAPH_ROUTE) {
        composable(route = LoginNav.route) {
            val viewModel =
                composableActivityViewModel<LoginViewModel>(
                    "Login",
                    null
                )

            UserLoginScreen(
                navController = navController,
                modifier = modifier,
                onLoginClick = viewModel::onUserLoginClick
            )
        }
    }
}