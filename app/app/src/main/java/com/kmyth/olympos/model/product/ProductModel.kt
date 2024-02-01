package com.kmyth.olympos.model.product

data class ProductModel(
    val unique_product: Int,
    val unique_store_info: Int,
    val unique_product_group: Int,
    val product_name: String,
    val price: Int,
    val image: String,
    val description: String,
    val amount: Int
)
