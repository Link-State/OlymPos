package com.kmyth.olympos.model.product

data class OptionListResponseModel(
    val result: String,
    val code: Int,
    val option: List<OptionModel>
)
