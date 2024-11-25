package com.example.medreader.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Spinner
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.medreader.models.ItemLido
import com.example.medreader.R


class ItemLidoAdapter(private val itemList: MutableList<ItemLido>) :
    RecyclerView.Adapter<ItemLidoAdapter.ItemViewHolder>() {

    private lateinit var quantityOptions: Array<String>

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
        private val textItemNome: TextView = itemView.findViewById(R.id.itemName)
        private val spinnerQuantidade: Spinner = itemView.findViewById(R.id.quantitySpinner)

        fun bind(item: ItemLido) {
            textItemNome.text = item.nome_item

            // VERIFICAR A LOGICA DE OPÇÕES DA QUANTIDADE
            quantityOptions = Array(999) { i -> (i + 1).toString() }

            val adapter = ArrayAdapter(itemView.context, android.R.layout.simple_spinner_item, quantityOptions)
            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
            spinnerQuantidade.adapter = adapter

            val initialPosition = item.quantidade_lida - 1
            spinnerQuantidade.setSelection(if (initialPosition >= 0) initialPosition else 0)

            spinnerQuantidade.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
                override fun onItemSelected(parent: AdapterView<*>, view: View?, position: Int, id: Long) {
                    item.quantidade_lida = quantityOptions[position].toInt()
                }

                override fun onNothingSelected(parent: AdapterView<*>) {}
            }
        }
    }
}