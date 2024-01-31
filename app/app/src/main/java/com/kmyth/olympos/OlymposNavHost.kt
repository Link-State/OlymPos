package com.kmyth.olympos

import androidx.activity.ComponentActivity
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import com.kmyth.olympos.view.login.navigation.loginNavGraph

@Composable
fun OlymposNavHost(
    navController: NavHostController,
    modifier: Modifier,
    dataStore: DataStore<Preferences>
) {
    NavHost(
        navController = navController,
        startDestination = LOGIN_GRAPH_ROUTE,
        modifier = modifier
    ) {
        loginNavGraph(navController = navController, modifier = modifier, dataStore = dataStore)
    }
}

@Composable
fun getActivity() = LocalContext.current as ComponentActivity

@Composable
inline fun <reified VM : ViewModel> composableActivityViewModel(
    key: String? = null,
    factory: ViewModelProvider.Factory? = null
): VM = viewModel(
    VM::class.java,
    getActivity(),
    key,
    factory
)