package com.kmyth.olympos.network

import com.kmyth.olympos.model.login.UserLoginRequestModel
import com.kmyth.olympos.model.login.UserLoginResponseModel
import com.kmyth.olympos.model.login.TableLoginRequestModel
import com.kmyth.olympos.model.login.TableLoginResponseModel
import com.kmyth.olympos.model.product.GroupListResponseModel
import com.kmyth.olympos.model.product.OptionListResponseModel
import com.kmyth.olympos.model.product.ProductListResponseModel
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Headers
import retrofit2.http.POST
import retrofit2.http.QueryMap

interface ServerCallInterface {

    /**
     * 사용자 로그인
     */
    @Headers("Content-Type: application/json")
    @POST("user-login")
    fun userLogin(@Body userInfo: UserLoginRequestModel): Call<UserLoginResponseModel>

    /**
     * 매장&테이블 로그인
     */
    @Headers("Content-Type: application/json")
    @POST("table-login")
    fun tableLogin(@Body tableInfo: TableLoginRequestModel): Call<TableLoginResponseModel>

    /**
     * 상품 카테고리 목록 불러옴
     */
    @Headers("Content-Type: application/json")
    @GET("get-group-list")
    @JvmSuppressWildcards
    fun getGroupList(@QueryMap storeInfo: Map<String, Any>): Call<GroupListResponseModel>

    /**
     * 상품 목록 불러옴
     */
    @Headers("Content-Type: application/json")
    @GET("get-product-list")
    @JvmSuppressWildcards
    fun getProductList(@QueryMap storeInfo: Map<String, Any>): Call<ProductListResponseModel>

    /**
     * 옵션 목록 불러옴
     */
    @Headers("Content-Type: application/json")
    @GET("get-option-list")
    @JvmSuppressWildcards
    fun getOptionList(@QueryMap storeInfo: Map<String, Any>): Call<OptionListResponseModel>

}