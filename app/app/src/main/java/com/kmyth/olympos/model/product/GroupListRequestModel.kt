package com.kmyth.olympos.model.product

data class GroupListRequestModel(
    val SSAID: String,
    val store_uid: Int
) {
    fun toMap(): Map<String, Any> {
        return mapOf(
            "SSAID" to SSAID,
            "store_uid" to store_uid
        )
    }
}
