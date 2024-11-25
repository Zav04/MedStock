package com.example.medreader.models

data class APIResponse<T>(
    val response: Boolean,
    val data: T?,
    val error: String?
)

data class Requerimento(
    val requerimento_id: Int,
    val setor_nome_localizacao: String,
    val nome_utilizador_pedido: String,
    val status: Int,
    val urgente: Boolean,
    val itens_pedidos: List<ItemPedido>,
    val data_pedido: String
)

data class ItemPedido(
    val nome_item: String,
    val quantidade: Int,
    val tipo_item: String,
)

data class ItemLido(
    val nome_item: String,
    var quantidade_lida: Int
)

//data class Item(
//    val nome_item: String,
//    val nome_tipo: String,
//    val codigo: String
//)