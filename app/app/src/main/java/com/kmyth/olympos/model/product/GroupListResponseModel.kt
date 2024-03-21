package com.kmyth.olympos.model.product

import com.google.gson.annotations.SerializedName

data class GroupListResponseModel(
    @SerializedName("result")
    val result: String,
    @SerializedName("code")
    val code: Int,
    @SerializedName("groups")
    val groups: List<GroupModel>
)
