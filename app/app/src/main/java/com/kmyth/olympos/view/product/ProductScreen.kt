package com.kmyth.olympos.view.product

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.Base64
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.itemsIndexed
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.ExperimentalComposeUiApi
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Devices
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
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
    var product by remember { mutableStateOf(
        // TODO : tmp Data
        ProductModel(0, 0, 0,
            "tmp", 10000, "", "desc",
            0, emptyList()
        )
    ) }
    var showProductDetail by remember { mutableStateOf(false) }
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
    val onProductClick: (ProductModel) -> Unit = { model ->
        product = model
        showProductDetail = true
    }
    val onDialogDismiss: () -> Unit = {
        showProductDetail = false
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
            productList,
            onProductClick
        )
    }

    if (showProductDetail) {
        ProductDetailDialog(product, onDialogDismiss)
    }
}

@Composable
fun ProductView(
    groupList: List<GroupModel>, 
    onGroupChanged: (Int) -> Unit, 
    productList: List<ProductModel>,
    onProductClick: (ProductModel) -> Unit
) {
    Column(
        modifier = Modifier
            .width(768.dp)
            .fillMaxHeight()
    ) {
        GroupListRow(groupList, onGroupChanged)
        ProductListBox(productList, onProductClick)
    }
}

@Composable
fun GroupListRow(
    groupList: List<GroupModel>, 
    onGroupChanged: (Int) -> Unit
) {
    LazyRow {
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
fun ProductListBox(
    productList: List<ProductModel>,
    onProductClick: (ProductModel) -> Unit
) {
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
                onClick = { onProductClick(product) }
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(0.dp),
                    verticalArrangement = Arrangement.SpaceBetween
                ) {
                    val decodedString = Base64.decode(product.image, Base64.DEFAULT) ?: ByteArray(0)
                    val decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.size) ?: createBitmap(224, 224)

                    Text(
                        modifier = Modifier.align(Alignment.Start),
                        text = product.product_name,
                        fontSize = 24.sp
                    )
                    ProductImage(
                        width = 192,
                        height = 108,
                        imageBitmap = decodedByte,
                        name = product.product_name
                    )
                    Text(
                        modifier = Modifier.align(Alignment.End),
                        text = "${product.price}",
                        fontSize = 24.sp
                    )
                }
            }
        }
    }
}

@Composable
fun ProductImage(
    width: Int,
    height: Int,
    imageBitmap: Bitmap,
    name: String
) {
    Box {
        Box(
            modifier = Modifier
                .width(width.dp)
                .height(height.dp)
                .align(Alignment.Center)
                .background(Color.Gray)
        )
        Image(
            modifier = Modifier
                .width(width.dp)
                .height(height.dp)
                .align(Alignment.Center),
            bitmap = imageBitmap.asImageBitmap(),
            contentDescription = "Image of $name",
            contentScale = ContentScale.Fit
        )
    }
}

@OptIn(ExperimentalComposeUiApi::class)
@Composable
fun ProductDetailDialog(
    product: ProductModel,
    onDialogDismiss: () -> Unit
) {
    Dialog(
        onDismissRequest = onDialogDismiss,
        properties = DialogProperties(
            dismissOnBackPress = true,
            dismissOnClickOutside = true,
            usePlatformDefaultWidth = false
        ),
        content = {
            ProductDetailDialogContent(
                product,
                onDialogDismiss
            )
        }
    )
}

@Composable
fun ProductDetailDialogContent(
    product: ProductModel,
    onDialogDismiss: () -> Unit
) {
    val decodedString = Base64.decode(product.image, Base64.DEFAULT) ?: ByteArray(0)
    val decodedByte = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.size) ?: createBitmap(224, 224)

    Surface(
        modifier = Modifier
            .width(1120.dp)
            .height(576.dp),
        color = Color.White
    ) {
        Row(
            modifier = Modifier.padding(44.dp)
        ) {
            Column(
                modifier = Modifier.width(548.dp)
            ) {
                Text(
                    text = product.product_name,
                    fontSize = 40.sp
                )
                Spacer(modifier = Modifier.height(24.dp))
                ProductImage(
                    width = 548,
                    height = 308,
                    imageBitmap = decodedByte,
                    name = product.product_name
                )
                Spacer(modifier = Modifier.height(24.dp))
                Text(
                    text = product.description,
                    fontSize = 24.sp
                )
            }
            Spacer(modifier = Modifier.width(76.dp))
            Column(
                modifier = Modifier.width(400.dp),
                horizontalAlignment = Alignment.End
            ) {
                Button( // TODO : Change to Image Button
                    modifier = Modifier
                        .width(28.dp)
                        .height(28.dp),
                    onClick = onDialogDismiss
                ) {
                    Text(text = "X")
                }
                Spacer(modifier = Modifier.height(40.dp))
                Box {
                    Box(
                        modifier = Modifier
                            .width(400.dp)
                            .height(424.dp)
                            .align(Alignment.Center)
                            .background(Color.LightGray)
                            .border(2.dp, Color.Gray)
                    )
                    Column(
                        modifier = Modifier
                            .align(Alignment.BottomCenter)
                    ) {
                        Box(
                            modifier = Modifier
                                .align(Alignment.CenterHorizontally)
                        ) {
                            Box(
                                modifier = Modifier
                                    .width(352.dp)
                                    .height(64.dp)
                                    .align(Alignment.TopCenter)
                                    .shadow(10.dp)
                                    .background(
                                        Color.White,
                                        RoundedCornerShape(15.dp, 15.dp, 0.dp, 0.dp)
                                    ),
                            )
                            Text(
                                modifier = Modifier
                                    .align(Alignment.TopStart)
                                    .offset(24.dp, 8.dp),
                                text = "총",
                                fontSize = 28.sp
                            )
                            Text(
                                modifier = Modifier
                                    .align(Alignment.TopEnd)
                                    .offset((-24).dp, 8.dp),
                                text = "${product.price}원",
                                fontSize = 28.sp
                            )
                        }
                        Button(
                            modifier = Modifier
                                .width(400.dp)
                                .height(64.dp),
                            shape = RectangleShape,
                            onClick = { /*TODO*/ }
                        ) {
                            Text(
                                text = "장바구니 추가",
                                fontSize = 32.sp
                            )
                        }
                    }
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

@Preview(
    showBackground = true,
    showSystemUi = true,
    device = Devices.TABLET)
@Composable
fun ProductDetailDialogPreview() {
    OlymPosTheme{
        ProductDetailDialogContent(
            ProductModel(
                0, 0, 0,
                "메뉴명", 10000, "",
                "메뉴 설명", 1, emptyList()
            )
        ) {}
    }
}