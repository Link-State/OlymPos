package com.kmyth.olympos.model.product

data class SuboptionModel(
    val unique_product_suboption: Int,
    val unique_product_option: Int,
    val suboption_name: String,
    val price: Int,
    val amount: Int
)
