package com.kmyth.olympos.view.login

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.material3.Button
import androidx.compose.material3.LocalTextStyle
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Devices
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import androidx.navigation.compose.rememberNavController
import com.kmyth.olympos.R
import com.kmyth.olympos.Store
import com.kmyth.olympos.ui.theme.OlymPosTheme

@Composable
fun LoginScreen(navController: NavHostController, modifier: Modifier) {

    var id by rememberSaveable { mutableStateOf("") }
    var pw by rememberSaveable { mutableStateOf("") }
    val maxChar = 32

    Box(
        modifier = modifier,
        contentAlignment = Alignment.Center
    ) {
        Column(
            modifier = Modifier
                .width(width = 1280.dp)
                .height(height = 480.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            // TODO: 로고 이미지 적용
            // Title
            Text(
                text = "OlymPos",
                color = Color.Black,
                textAlign = TextAlign.Center,
                style = TextStyle(
                    fontSize = 64.sp),
                modifier = Modifier
                    .wrapContentHeight(align = Alignment.CenterVertically)
                    .padding(0.dp, 0.dp, 0.dp, 32.dp))

            // ID
            TextField(
                modifier = Modifier
                    .width(width = 480.dp)
                    .height(height = 96.dp)
                    .padding(0.dp, 0.dp, 0.dp, 8.dp),
                textStyle = LocalTextStyle.current.copy(fontSize = 36.sp),
                value = id,
                onValueChange = { if (it.length <= maxChar) id = it },
                placeholder = { Text(stringResource(id = R.string.id)) })

            // Password
            TextField(
                modifier = Modifier
                    .width(width = 480.dp)
                    .height(height = 96.dp)
                    .padding(0.dp, 0.dp, 0.dp, 16.dp),
                textStyle = LocalTextStyle.current.copy(fontSize = 36.sp),
                value = pw,
                onValueChange = { if (it.length <= maxChar) pw = it },
                placeholder = { Text(stringResource(id = R.string.password)) })

            // Login btn
            Button(
                modifier = Modifier
                    .width(width = 480.dp)
                    .height(height = 96.dp),
                onClick = {
                    // TODO: 유효성 체크
                    // TODO: 통신
                    navController.navigate(Store.route)
                }) {
                Text(
                    text = stringResource(id = R.string.login),
                    fontSize = 32.sp
                )
            }
        }
    }
}

@Preview(
    showBackground = true,
    showSystemUi = true,
    device = Devices.TABLET)
@Composable
fun LoginScreenPreview() {
    OlymPosTheme {
        LoginScreen(
            navController = rememberNavController(),
            modifier = Modifier.fillMaxSize()
        )
    }
}