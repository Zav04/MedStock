package com.example.medreader.api

import com.example.medreader.models.APIResponse
import com.example.medreader.models.Requerimento
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Query


interface RequerimentosApi {

    @GET("MedStock_GetRequerimentosByUser/")
    fun getRequerimentosByUser(@Query("user_id") userId: Int): Call<APIResponse<List<Requerimento>>>
}