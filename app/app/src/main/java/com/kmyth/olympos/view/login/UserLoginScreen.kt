package com.kmyth.olympos.view.login

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentHeight
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
import com.kmyth.olympos.TableNav
import com.kmyth.olympos.model.login.UserLoginRequestModel
import com.kmyth.olympos.ui.theme.DefaultButton
import com.kmyth.olympos.ui.theme.OlymPosTheme
import timber.log.Timber

@Composable
fun UserLoginScreen(
    navController: NavHostController,
    modifier: Modifier,
    onLoginClick: ((UserLoginRequestModel, (String) -> Unit) -> Unit)?
) {

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
            // TODO : 마스킹 기능
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
            DefaultButton(title = stringResource(id = R.string.login), enabled = true) {
                // TODO: 유효성 체크
                // TODO : DataStore 저장
                if (onLoginClick != null) {
                    Timber.d("onClick $id, $pw")
                    onLoginClick(
                        UserLoginRequestModel(id, pw)
                    ) { navController.navigate("${TableNav.route}/$it") }
                }
            }
        }
    }
}

@Preview(
    showBackground = true,
    showSystemUi = true,
    device = Devices.TABLET)
@Composable
fun UserLoginScreenPreview() {
    OlymPosTheme {
        UserLoginScreen(
            navController = rememberNavController(),
            modifier = Modifier.fillMaxSize(),
            null
        )
    }
}