package com.kmyth.olympos.model.product

data class ProductListRequestModel(
    val store_uid: Int
) {
    fun toMap(): Map<String, Any> {
        return mapOf(
            "store_uid" to store_uid
        )
    }
}
