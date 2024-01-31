package com.kmyth.olympos.model.login

import com.google.gson.annotations.SerializedName

data class UserLoginResponseModel(
    @SerializedName("result")
    val result: String,
    @SerializedName("code")
    val code: Int,
    @SerializedName("stores")
    val stores: List<StoreModel>
)
