package com.kmyth.olympos.view.product

import android.graphics.BitmapFactory
import android.util.Base64
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.itemsIndexed
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Devices
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.graphics.createBitmap
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.navigation.NavHostController
import androidx.navigation.compose.rememberNavController
import com.kmyth.olympos.getSSAID
import com.kmyth.olympos.model.product.GroupModel
import com.kmyth.olympos.model.product.OptionModel
import com.kmyth.olympos.model.product.ProductModel
import com.kmyth.olympos.ui.theme.OlymPosTheme
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

@Composable
fun ProductScreen(
    navController: NavHostController,
    modifier: Modifier,
    updateProduct: ((String) -> Unit)?,
    groupListStateFlow: StateFlow<List<GroupModel>>,
    productListStateFlow: StateFlow<List<ProductModel>>,
    optionListStateFlow: StateFlow<List<OptionModel>>
) {
    val context = LocalContext.current
    val groupListState = groupListStateFlow.collectAsStateWithLifecycle()
    val productListState = productListStateFlow.collectAsStateWithLifecycle()
    val optionListState = optionListStateFlow.collectAsStateWithLifecycle()

    var groupIdx by remember { mutableStateOf(
        groupListState.value.firstOrNull()?.unique_product_group ?: 0
    ) }
    var productList by remember { mutableStateOf(
        productListState.value.filter {
            it.unique_product_group == groupIdx
        }
    ) }
    val onGroupChanged: (Int) -> Unit = { index ->
        groupIdx = index

        if (productListState.value.size > groupIdx) {
            productList = productListState.value.filter {
                it.unique_product_group == groupIdx
            }
        } else {
            productList = emptyList()
        }
    }

    LaunchedEffect(Unit) {
        if (updateProduct != null) {
            updateProduct(getSSAID(context))
        }
    }

    Row(
        modifier = modifier.padding(48.dp, 36.dp)
    ) {
        ProductView(
            groupListState.value,
            onGroupChanged,
            productList
        )
    }
}

@Composable
fun ProductView(
    groupList: List<GroupModel>, 
    onGroupChanged: (Int) -> Unit, 
    productList: List<ProductModel>
) {
    Column(
        modifier = Modifier
            .width(768.dp)
            .fillMaxHeight()
    ) {
        GroupListRow(groupList, onGroupChanged)
        ProductListBox(productList)
    }
}

@Composable
fun GroupListRow(
    groupList: List<GroupModel>, 
    onGroupChanged: (Int) -> Unit
) {
    LazyRow() {
        itemsIndexed(groupList) { _, group ->
            Button(
                modifier = Modifier
                    .width(192.dp)
                    .height(72.dp),
                shape = RectangleShape,
                onClick = { onGroupChanged(group.unique_product_group) }
            ) {
                Text(
                    text = group.group_name,
                    fontSize = 32.sp
                )
            }
        }
    }
}

@Composable
fun ProductListBox(productList: List<ProductModel>) {
    LazyVerticalGrid(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.LightGray),
        columns = GridCells.Fixed(3),
        contentPadding = PaddingValues(24.dp),
        verticalArrangement = Arrangement.spacedBy(24.dp),
        horizontalArrangement = Arrangement.spacedBy(24.dp)
    ) {
        itemsIndexed(productList) { _, product ->
            Button(
                modifier = Modifier
                    .width(224.dp)
                    .height(224.dp),
                contentPadding = PaddingValues(16.dp),
                shape = RoundedCornerShape(8.dp),
                onClick = {}) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(0.dp)
                ) {
                    val decodedString = Base64.decode(product.image, Base64.DEFAULT) ?: ByteArray(0)
                    val decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.size) ?: createBitmap(224, 224)

                    Text(
                        modifier = Modifier.align(Alignment.TopStart),
                        text = product.product_name,
                        fontSize = 24.sp
                    )
                    Box(
                        modifier = Modifier
                            .width(192.dp)
                            .height(108.dp)
                            .align(Alignment.Center)
                            .background(Color.Gray)
                    )
                    Image(
                        modifier = Modifier
                            .width(192.dp)
                            .height(108.dp)
                            .align(Alignment.Center),
                        bitmap = decodedByte.asImageBitmap(),
                        contentDescription = "Image of ${product.product_name}",
                        contentScale = ContentScale.Fit
                    )
                    Text(
                        modifier = Modifier.align(Alignment.BottomEnd),
                        text = "${product.price}",
                        fontSize = 24.sp
                    )
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
fun ProductScreenPreview() {
    OlymPosTheme {
        ProductScreen(
            navController = rememberNavController(),
            modifier = Modifier.fillMaxSize(),
            updateProduct = null,
            groupListStateFlow = MutableStateFlow<List<GroupModel>>(emptyList()).asStateFlow(),
            productListStateFlow = MutableStateFlow<List<ProductModel>>(emptyList()).asStateFlow(),
            optionListStateFlow = MutableStateFlow<List<OptionModel>>(emptyList()).asStateFlow()
        )
    }
}