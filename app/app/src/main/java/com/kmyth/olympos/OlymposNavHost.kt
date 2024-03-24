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
import androidx.navigation.compose.composable
import com.kmyth.olympos.view.login.navigation.loginNavGraph
import com.kmyth.olympos.view.product.ProductScreen
import com.kmyth.olympos.viewmodel.login.UserPreferencesRepository
import com.kmyth.olympos.viewmodel.product.ProductRepositoryImpl
import com.kmyth.olympos.viewmodel.product.ProductViewModel
import com.kmyth.olympos.viewmodel.product.ProductViewModelFactory

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

        composable(route = ProductNav.route) {
            val viewModel =
                composableActivityViewModel<ProductViewModel>(
                    "Product",
                    ProductViewModelFactory(
                        ProductRepositoryImpl(),
                        UserPreferencesRepository(dataStore)
                    )
                )
            ProductScreen(
                navController = navController,
                modifier = modifier,
                getGroupList = viewModel::getGroupList,
                groupListStateFlow = viewModel.groupListState
            )
        }
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