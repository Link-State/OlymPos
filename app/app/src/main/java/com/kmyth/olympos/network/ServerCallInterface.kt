package com.kmyth.olympos.network

import com.kmyth.olympos.model.login.UserLoginRequestModel
import com.kmyth.olympos.model.login.UserLoginResponseModel
import com.kmyth.olympos.model.login.TableLoginRequestModel
import com.kmyth.olympos.model.login.TableLoginResponseModel
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.Headers
import retrofit2.http.POST

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

}