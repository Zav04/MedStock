package com.example.medreader.api

import com.example.medreader.models.APIResponse
import com.example.medreader.models.Requerimento
import com.example.medreader.models.UpdateRequerimentoRequest
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PUT

interface RequerimentosApi {

    @GET("MedReader_Requerimentos/")
    fun getRequerimentos(): Call<APIResponse<List<Requerimento>>>

    @PUT("MedReader_Update_Requerimento_Preparacao/")
    fun updateRequerimentoPreparacao(@Body payload: UpdateRequerimentoRequest): Call<APIResponse<String>>
}
