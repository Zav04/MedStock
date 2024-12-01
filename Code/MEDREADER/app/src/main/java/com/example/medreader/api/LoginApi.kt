package com.example.medreader.api

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST
import com.example.medreader.models.LoginRequest
import com.example.medreader.models.LoginResponse

interface LoginApi {

    @POST("/MedReader_Login/")
    fun loginUser(@Body loginRequest: LoginRequest): Call<LoginResponse>
}