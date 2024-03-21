package com.kmyth.olympos.model.product

data class ProductListResponseModel(
    val result: String,
    val code: Int,
    val products: List<ProductModel>
)
