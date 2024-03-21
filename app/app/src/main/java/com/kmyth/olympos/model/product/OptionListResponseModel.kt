package com.kmyth.olympos.model.product

import com.google.gson.annotations.SerializedName

data class OptionListResponseModel(
    @SerializedName("result")
    val result: String,
    @SerializedName("code")
    val code: Int,
    @SerializedName("options")
    val options: List<OptionModel>
)
