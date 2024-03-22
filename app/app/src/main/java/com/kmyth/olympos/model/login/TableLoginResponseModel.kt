package com.kmyth.olympos.model.login

import com.google.gson.annotations.SerializedName

data class TableLoginResponseModel(
    @SerializedName("result")
    val result: String,
    @SerializedName("code")
    val code: Int
)
