package com.example.medreader.models
import android.os.Parcelable
import kotlinx.parcelize.Parcelize

data class APIResponse<T>(
    val response: Boolean,
    val data: T?,
    val error: String?
)

data class LoginRequest(
    val email: String,
    val password: String
)

data class LoginResponse(
    val response: Boolean,
    val error: String?,
    val data: UserData?
)

data class UserData(
    val id: Int,
    val name: String,
    val email: String,
    val role: String
)

data class UpdateRequerimentoRequest(
    val user_id: Int,
    val requerimento_id: Int
)

data class Requerimento(
    val requerimento_id: Int,
    val itens_pedidos: List<ItemPedido>
)

@Parcelize
data class ItemPedido(
    val nome_item: String,
    val codigo: String,
    val quantidade: Int
) : Parcelable

data class ItemLido(
    val nome_item: String,
    val codigo: String = "",
    var quantidade_lida: Int
)