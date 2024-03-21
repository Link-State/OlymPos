package com.kmyth.olympos.model.product

data class OptionModel(
    val unique_product_option: Int,
    val unique_store_info: Int,
    val option_name: String,
    val price: Int,
    val suboption_offer: Int
)
