package com.kmyth.olympos.model.login

data class StoreModel(
    val unique_admin: Int,
    val store_name: String,
    val store_owner: String,
    val store_address: String,
    val store_tel_number: String,
    val table_count: Int,
    val last_modify_date: String?
)