package com.kmyth.olympos.model.login

import com.google.gson.annotations.SerializedName
import com.kmyth.olympos.model.product.ProductModel

data class TableLoginResponseModel(
    @SerializedName("result")
    val result: String,
    @SerializedName("code")
    val code: Int,
    @SerializedName("products")
    val products: List<ProductModel>
)
