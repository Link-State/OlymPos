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
import androidx.navigation.compose.rememberNavController
import com.kmyth.olympos.ui.theme.OlymPosTheme
import com.kmyth.olympos.view.login.LoginScreen

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            OlymPosTheme {

                val navController = rememberNavController()
                val startDestination = getStartDestination()
                val modifier = Modifier.fillMaxSize()

                OlymposNavHost(navController, startDestination, modifier)
            }
        }
    }

    /**
     * 시작 화면 가져오기
     */
    private fun getStartDestination(): String {
        var startDestination = Login.route
        val prefs = this.getPreferences(Context.MODE_PRIVATE)
        val isLogin = prefs.getBoolean(getString(R.string.pref_login), false)

        // 로그인 이력이 있으면 로그인 건너뛰기
        if (isLogin) {
            val isSelectStore = prefs.getInt(getString(R.string.pref_store), -1)
            if (isSelectStore != -1) {
                val isSelectTable = prefs.getInt(getString(R.string.pref_table), -1)
                if (isSelectTable != -1) {
                    // TODO: 메뉴 화면 연결
                } else {
                    startDestination = Table.route
                }
            } else {
                startDestination = Store.route
            }
        }

        return startDestination
    }
}

@Preview(
    showBackground = true,
    showSystemUi = true,
    device = Devices.TABLET)
@Composable
fun MainPreview() {
    OlymPosTheme {
        LoginScreen(
            navController = rememberNavController(),
            modifier = Modifier.fillMaxSize()
        )
    }
}