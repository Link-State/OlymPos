package com.kmyth.olympos.model.login

import com.kmyth.olympos.model.product.ProductModel

data class TableLoginResponseModel(
    val result: String,
    val code: Int,
    val products: List<ProductModel>
)
