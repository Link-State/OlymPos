package com.kmyth.olympos.view.product

import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Devices
import androidx.compose.ui.tooling.preview.Preview
import androidx.navigation.NavHostController
import androidx.navigation.compose.rememberNavController
import com.google.gson.Gson
import com.kmyth.olympos.model.product.ProductModel
import com.kmyth.olympos.ui.theme.OlymPosTheme

@Composable
fun ProductScreen(
    navController: NavHostController,
    modifier: Modifier,
    productList: List<ProductModel>
) {
    Text(text = Gson().toJson(productList))
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
            listOf()
        )
    }
}