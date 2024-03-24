package com.kmyth.olympos.view.product

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Devices
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController
import androidx.navigation.compose.rememberNavController
import com.kmyth.olympos.getSSAID
import com.kmyth.olympos.model.product.GroupModel
import com.kmyth.olympos.ui.theme.OlymPosTheme
import kotlinx.coroutines.flow.StateFlow

@Composable
fun ProductScreen(
    navController: NavHostController,
    modifier: Modifier,
    getGroupList: ((String) -> Unit)?,
    groupListStateFlow: StateFlow<List<GroupModel>>?
) {
    val context = LocalContext.current
    val groupListState = groupListStateFlow?.collectAsState()
    if (getGroupList != null) {
        getGroupList(getSSAID(context))
    }

    Text(
        text = "${groupListState?.value} To be continued... Groups, Products, Options",
        fontSize = 32.sp
    )
}

@Preview(
    showBackground = true,
    showSystemUi = true,
    device = Devices.TABLET)
@Composable
fun ProductScreenPreview() {
    OlymPosTheme {
        ProductScreen(
            navController = rememberNavController(),
            modifier = Modifier.fillMaxSize(),
            getGroupList = null,
            groupListStateFlow = null
        )
    }
}