package com.kmyth.olympos.model.product

data class GroupListResponseModel(
    val result: String,
    val code: Int,
    val groups: List<GroupModel>
)
