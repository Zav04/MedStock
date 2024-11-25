package com.example.medreader.adapter

import android.content.Context
import android.content.Intent
import android.graphics.Typeface
import android.util.TypedValue
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.medreader.models.Requerimento
import com.example.medreader.R
import com.example.medreader.ScanActivity
import java.text.SimpleDateFormat
import java.util.Locale


class RequerimentoAdapter(
    private val context: Context,
    private val requerimentos: List<Requerimento>
) : RecyclerView.Adapter<RequerimentoAdapter.ViewHolder>() {

    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvRequerimentoId: TextView = itemView.findViewById(R.id.tvRequerimentoId)
        val tvSetorNome: TextView = itemView.findViewById(R.id.tvSetorNome)
        val tvNomeUtilizador: TextView = itemView.findViewById(R.id.tvNomeUtilizador)
        val tvDataPedido: TextView = itemView.findViewById(R.id.tvDataPedido)
        val tvUrgente: TextView = itemView.findViewById(R.id.tvUrgente)
        val btnComecarScan: Button = itemView.findViewById(R.id.btnComecarScan)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_requerimento, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val requerimento = requerimentos[position]

        holder.tvRequerimentoId.text = "ID: ${requerimento.requerimento_id}"
        holder.tvSetorNome.text = "Setor: ${requerimento.setor_nome_localizacao}"
        holder.tvNomeUtilizador.text = "Utilizador: ${requerimento.nome_utilizador_pedido}"

        val inputFormat = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault())
        val outputFormat = SimpleDateFormat("dd/MM/yyyy HH:mm:ss", Locale.getDefault())
        val formattedDate = try {
            val date = inputFormat.parse(requerimento.data_pedido)
            outputFormat.format(date)
        } catch (e: Exception) {
            requerimento.data_pedido
        }

        holder.tvDataPedido.text = "Data: $formattedDate"

        if (requerimento.urgente) {
            holder.tvUrgente.visibility = View.VISIBLE
            holder.tvUrgente.text = "Urgente!"

            holder.tvUrgente.setTextSize(TypedValue.COMPLEX_UNIT_SP, 18f)
            holder.tvUrgente.setTypeface(null, Typeface.BOLD)
        } else {
            holder.tvUrgente.visibility = View.GONE
        }

        holder.btnComecarScan.setOnClickListener {
            val intent = Intent(context, ScanActivity::class.java)
            intent.putExtra("requerimentoId", requerimento.requerimento_id)
            context.startActivity(intent)
        }
    }

    override fun getItemCount(): Int = requerimentos.size
}