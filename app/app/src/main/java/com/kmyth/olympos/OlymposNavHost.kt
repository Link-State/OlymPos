package com.kmyth.olympos

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.kmyth.olympos.view.login.LoginScreen
import com.kmyth.olympos.view.login.SelectStoreScreen
import com.kmyth.olympos.view.login.SelectTableScreen

@Composable
fun OlymposNavHost(
    navController: NavHostController,
    startDestination: String,
    modifier: Modifier
) {
    NavHost(
        navController = navController,
        startDestination = startDestination,
        modifier = modifier
    ) {
        composable(route = Login.route) {
            LoginScreen(
                navController = navController,
                modifier = modifier
            )
        }
        composable(route = Store.route) {
            SelectStoreScreen(
                navController = navController,
                modifier = modifier
            )
        }
        composable(route = Table.route) {
            SelectTableScreen(
                navController = navController,
                modifier = modifier
            )
        }
    }
}