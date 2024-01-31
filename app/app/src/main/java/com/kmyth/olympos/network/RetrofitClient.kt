package com.kmyth.olympos.network

import com.kmyth.olympos.BuildConfig
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitClient {

    private const val baseUrl = BuildConfig.BASE_URL
    private var retrofit: Retrofit? = null

    fun getClient(): Retrofit? {
        if (retrofit == null) {
            val okHttpClient =
                OkHttpClient
                    .Builder()
                    .addInterceptor(Interceptor {
                        val original = it.request()
                        val request = original.newBuilder()
                            .build()
                        return@Interceptor it.proceed(request)
                    })
                    .build()

            return Retrofit.Builder()
                .baseUrl(baseUrl)
                .client(okHttpClient)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
        }

        return retrofit
    }
}