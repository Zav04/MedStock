package com.example.medreader.connection

import com.example.medreader.api.LoginApi
import com.example.medreader.api.RequerimentosApi
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit


object RetrofitClient {
    private const val BASE_URL = "https://medstock-api-ce98.onrender.com/"

    private val client: OkHttpClient = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    val retrofit: Retrofit = Retrofit.Builder()
        .baseUrl(BASE_URL)
        .client(client)
        .addConverterFactory(GsonConverterFactory.create())
        .build()


    val requeimentosApi: RequerimentosApi by lazy {
        retrofit.create(RequerimentosApi::class.java)
    }

    val loginApi: LoginApi by lazy {
        retrofit.create(LoginApi::class.java)
    }
}