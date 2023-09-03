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
import com.kmyth.olympos.Table
import com.kmyth.olympos.ui.theme.OlymPosTheme

@Composable
fun SelectStoreScreen(navController: NavHostController, modifier: Modifier) {
    OlymPosTheme {
        SelectScreen(
            stringResource(R.string.store_select),
            listOf("양고기집", "닭고기집", "소고기집", "토끼고기집"), // TODO: TEST Value
            {
                // TODO: 통신
                navController.navigate(Table.route)
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
fun SelectStoreScreenPreview() {
    OlymPosTheme {
        SelectStoreScreen(
            navController = rememberNavController(),
            modifier = Modifier.fillMaxSize()
        )
    }
}