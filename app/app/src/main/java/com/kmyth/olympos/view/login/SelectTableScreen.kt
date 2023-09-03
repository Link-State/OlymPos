package com.kmyth.olympos.view.login

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Devices
import androidx.compose.ui.tooling.preview.Preview
import androidx.navigation.NavHostController
import androidx.navigation.compose.rememberNavController
import com.kmyth.olympos.R
import com.kmyth.olympos.ui.theme.OlymPosTheme

@Composable
fun SelectTableScreen(navController: NavHostController, modifier: Modifier) {
    OlymPosTheme {
        SelectScreen(
            stringResource(R.string.table_select),
            listOf("1", "2", "3", "4"), // TODO: TEST Value
            {
                // TODO: 통신
                // TODO: 메뉴 화면 연결
            },
            modifier = modifier
        )
    }
}

@Preview(
    showBackground = true,
    showSystemUi = true,
    device = Devices.TABLET)
@Composable
fun SelectTableScreenPreview() {
    OlymPosTheme {
        SelectTableScreen(
            navController = rememberNavController(),
            modifier = Modifier.fillMaxSize()
        )
    }
}