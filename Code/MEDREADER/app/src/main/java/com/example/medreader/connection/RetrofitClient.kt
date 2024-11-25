package com.example.medreader.connection

import com.example.medreader.api.RequerimentosApi
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory


object RetrofitClient {
    // IP da Máquina(PC)
    // Não sei como ligar de outra forma
    private const val BASE_URL = "http://192.168.1.188:8000/"

    val api: RequerimentosApi by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(RequerimentosApi::class.java)
    }
}