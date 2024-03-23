package com.kmyth.olympos.view.login

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Devices
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import androidx.navigation.compose.rememberNavController
import com.kmyth.olympos.ProductNav
import com.kmyth.olympos.R
import com.kmyth.olympos.getSSAID
import com.kmyth.olympos.model.login.StoreModel
import com.kmyth.olympos.model.login.TableLoginRequestModel
import com.kmyth.olympos.ui.theme.DefaultButton
import com.kmyth.olympos.ui.theme.DefaultMenuBox
import com.kmyth.olympos.ui.theme.OlymPosTheme
import timber.log.Timber

@Composable
fun TableLoginScreen(
    navController: NavHostController,
    modifier: Modifier,
    storeList: List<StoreModel>,
    onLoginClick: ((TableLoginRequestModel, () -> Unit) -> Unit)?
) {
    Box(
        modifier = modifier,
        contentAlignment = Alignment.Center
    ) {
        // 매장 목록이 없는 경우
        if (storeList.isEmpty()) {
            Column(
                modifier = Modifier
                    .width(width = 1280.dp)
                    .height(height = 480.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.SpaceBetween
            ) {
                SelectStoreText()
                EmptyListText()
                DefaultButton(
                    title = stringResource(R.string.select),
                    enabled = false
                ) {}
            }
        } else {
            // TODO : 테이블 목록 전환 안 되는 문제 수정
            val context = LocalContext.current
            val storePairList: List<Pair<Int, String>> =
                storeList.mapIndexed { index, store -> index to store.store_name }
            var selectedStore by remember { mutableStateOf(0) }
            var selectedTable by remember { mutableStateOf(1) }
            var tableList by remember { mutableStateOf(List(storeList[0].table_count) { it + 1 }) }
            var tablePairList: List<Pair<Int, String>> =
                tableList.mapIndexed { index, table -> (index + 1) to table.toString() }
            var enabledButton by remember { mutableStateOf(tableList.isNotEmpty()) }
            val updateStore: (Int) -> Unit = {
                Timber.d("updateStore $it")
                selectedStore = it
                selectedTable = 0
                tableList = List(storeList[selectedStore].table_count) { index -> index + 1 }
                tablePairList = tableList.mapIndexed { index, table ->
                    index to table.toString()
                }
                enabledButton = tableList.isNotEmpty()
            }
            val updateTable: (Int) -> Unit = {
                Timber.d("updateTable $it")
                selectedTable = it
            }
            Column(
                modifier = Modifier
                    .width(width = 1280.dp)
                    .height(height = 480.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.SpaceBetween
            ) {
                SelectStoreText()
                // 매장 목록
                DefaultMenuBox(storePairList, updateStore)
                // 테이블 목록
                DefaultMenuBox(tablePairList, updateTable)
                DefaultButton(
                    title = stringResource(id = R.string.select),
                    enabled = enabledButton,
                    onClick = {
                        if (onLoginClick != null) {
                            Timber.d("selectedStore ${storeList[selectedStore].unique_store_info}, selectedTable $selectedTable")
                            onLoginClick(
                                TableLoginRequestModel(getSSAID(context), storeList[selectedStore].unique_store_info, selectedTable)
                            ) {
                                navController.navigate(ProductNav.route)
                            }
                        }
                    }
                )
            }
        }
    }
}

@Composable
fun SelectStoreText() {
    Text(
        text = stringResource(id = R.string.store_select),
        color = Color.Black,
        textAlign = TextAlign.Center,
        style = TextStyle(
            fontSize = 64.sp
        ),
        modifier = Modifier
            .padding(0.dp, 0.dp, 0.dp, 32.dp)
            .wrapContentHeight(align = Alignment.CenterVertically)
    )
}

@Composable
fun EmptyListText() {
    Text(
        text = stringResource(id = R.string.empty_select),
        color = Color.Black,
        textAlign = TextAlign.Center,
        style = TextStyle(
            fontSize = 36.sp
        ),
        modifier = Modifier
            .fillMaxWidth()
            .padding(0.dp, 0.dp, 0.dp, 16.dp)
            .wrapContentHeight(align = Alignment.CenterVertically)
    )
}

@Preview(
    showBackground = true,
    showSystemUi = true,
    device = Devices.TABLET)
@Composable
fun TableLoginScreenPreview() {
    OlymPosTheme {
        TableLoginScreen(
            navController = rememberNavController(),
            modifier = Modifier.fillMaxSize(),
            listOf(),
            null
        )
    }
}