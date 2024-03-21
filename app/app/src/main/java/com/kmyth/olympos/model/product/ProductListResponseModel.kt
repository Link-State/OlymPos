package com.kmyth.olympos.model.product

import com.google.gson.annotations.SerializedName

data class ProductListResponseModel(
    @SerializedName("result")
    val result: String,
    @SerializedName("code")
    val code: Int,
    @SerializedName("products")
    val products: List<ProductModel>
)
