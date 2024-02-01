package com.kmyth.olympos.view.login.navigation

import androidx.compose.ui.Modifier
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.navigation.NavGraphBuilder
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.composable
import androidx.navigation.compose.navigation
import androidx.navigation.navArgument
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.kmyth.olympos.LOGIN_GRAPH_ROUTE
import com.kmyth.olympos.LoginNav
import com.kmyth.olympos.TableNav
import com.kmyth.olympos.composableActivityViewModel
import com.kmyth.olympos.model.login.StoreModel
import com.kmyth.olympos.view.login.TableLoginScreen
import com.kmyth.olympos.view.login.UserLoginScreen
import com.kmyth.olympos.viewmodel.login.LoginRepositoryImpl
import com.kmyth.olympos.viewmodel.login.LoginViewModel
import com.kmyth.olympos.viewmodel.login.LoginViewModelFactory
import com.kmyth.olympos.viewmodel.login.UserPreferencesRepository
import timber.log.Timber

fun NavGraphBuilder.loginNavGraph(
    navController: NavHostController,
    modifier: Modifier,
    dataStore: DataStore<Preferences>
) {
    navigation(startDestination = LoginNav.route, route = LOGIN_GRAPH_ROUTE) {
        composable(route = LoginNav.route) {
            val viewModel =
                composableActivityViewModel<LoginViewModel>(
                    "Login",
                    LoginViewModelFactory(
                        LoginRepositoryImpl(),
                        UserPreferencesRepository(dataStore)
                    )
                )

            UserLoginScreen(
                navController = navController,
                modifier = modifier,
                onLoginClick = viewModel::onUserLoginClick
            )
        }
        composable(
            route = TableNav.route+"/{storeList}",
            arguments = listOf(
                navArgument("storeList") {
                    type = NavType.StringType
                }
            )
        ) {
            if (it.arguments != null) {
                val viewModel =
                    composableActivityViewModel<LoginViewModel>(
                        "Login",
                        LoginViewModelFactory(
                            LoginRepositoryImpl(),
                            UserPreferencesRepository(dataStore)
                        )
                    )
                val storeStr = it.arguments!!.getString("storeList", "")
                Timber.d("storeStr $storeStr")
                val storeList = Gson().fromJson<List<StoreModel>>(storeStr, object: TypeToken<List<StoreModel>>(){}.type)

                TableLoginScreen(
                    navController = navController,
                    modifier = modifier,
                    storeList = storeList,
                    onLoginClick = viewModel::onTableLoginClick)
            } else {
                Timber.d("it.arguments == null")
            }
        }
    }
}