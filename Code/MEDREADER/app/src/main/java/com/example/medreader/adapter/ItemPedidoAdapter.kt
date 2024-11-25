package com.example.medreader.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.medreader.models.ItemPedido
import com.example.medreader.R


class ItemPedidoAdapter(private var itemList: List<ItemPedido>) :
    RecyclerView.Adapter<ItemPedidoAdapter.ItemViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ItemViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_pedido, parent, false)
        return ItemViewHolder(view)
    }

    override fun onBindViewHolder(holder: ItemViewHolder, position: Int) {
        val item = itemList[position]
        holder.bind(item)
    }

    override fun getItemCount(): Int {
        return itemList.size
    }

    inner class ItemViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val textNomeItem: TextView = itemView.findViewById(R.id.tvNomeItem)
        private val textQuantidadeItem: TextView = itemView.findViewById(R.id.tvQuantidadeItem)
        private val textTipoItem: TextView = itemView.findViewById(R.id.tvTipoItem)

        fun bind(item: ItemPedido) {
            textNomeItem.text = item.nome_item
            textQuantidadeItem.text = item.quantidade.toString()
            textTipoItem.text = item.tipo_item
        }
    }
}