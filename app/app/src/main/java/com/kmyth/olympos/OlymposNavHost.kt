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
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.kmyth.olympos.model.product.ProductModel
import com.kmyth.olympos.view.login.navigation.loginNavGraph
import com.kmyth.olympos.viewmodel.product.ProductRepositoryImpl
import com.kmyth.olympos.viewmodel.product.ProductViewModel
import com.kmyth.olympos.viewmodel.product.ProductViewModelFactory
import timber.log.Timber

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

        composable(route = ProductNav.route+"/{productList}",
            arguments = listOf(
                navArgument("productList") {
                    type = NavType.StringType
                }
            )
        ) {
            if (it.arguments != null) {
                val viewModel =
                    composableActivityViewModel<ProductViewModel>(
                        "Product",
                        ProductViewModelFactory(ProductRepositoryImpl())
                    )
                val productStr = it.arguments!!.getString("productList", "")
                Timber.d("productStr $productStr")
                val storeList = Gson().fromJson<List<ProductModel>>(productStr, object: TypeToken<List<ProductModel>>(){}.type)


            } else {
                Timber.d("ProductNav it.arguments == null")
            }
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