package com.example.medreader.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.medreader.models.ItemLido
import com.example.medreader.R

class ItemLidoAdapter(private val itemList: MutableList<ItemLido>, private val verificarItens: () -> Boolean) :
    RecyclerView.Adapter<ItemLidoAdapter.ItemViewHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ItemViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_lido, parent, false)
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
        private val textNomeItem: TextView = itemView.findViewById(R.id.nomeItemLido)
        private val textQuantidade: TextView = itemView.findViewById(R.id.quantidadeLida)
        private val decreaseButton: Button = itemView.findViewById(R.id.decreaseButton)
        private val increaseButton: Button = itemView.findViewById(R.id.increaseButton)

        fun bind(item: ItemLido) {
            textNomeItem.text = item.nome_item
            textQuantidade.text = item.quantidade_lida.toString()

            decreaseButton.setOnClickListener {
                if (item.quantidade_lida > 1) {
                    item.quantidade_lida--
                    textQuantidade.text = item.quantidade_lida.toString()
                    verificarItens()
                }
            }

            increaseButton.setOnClickListener {
                item.quantidade_lida++
                textQuantidade.text = item.quantidade_lida.toString()
                verificarItens()
            }
        }
    }
}