package com.kmyth.olympos

import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Devices
import androidx.compose.ui.tooling.preview.Preview
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.preferencesDataStore
import androidx.navigation.compose.rememberNavController
import com.kmyth.olympos.view.login.UserLoginScreen
import com.kmyth.olympos.ui.theme.OlymPosTheme
import timber.log.Timber

private const val USER_PREFERENCES = "user_preferences"

val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = USER_PREFERENCES)

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        Timber.plant(Timber.DebugTree())
        super.onCreate(savedInstanceState)
        setContent {
            OlymPosTheme {

                val navController = rememberNavController()
                val modifier = Modifier.fillMaxSize()

                OlymposNavHost(navController, modifier, dataStore)
            }
        }
    }
}

@Preview(
    showBackground = true,
    showSystemUi = true,
    device = Devices.TABLET)
@Composable
fun MainPreview() {
    OlymPosTheme {
        UserLoginScreen(
            navController = rememberNavController(),
            modifier = Modifier.fillMaxSize(),
            null
        )
    }
}