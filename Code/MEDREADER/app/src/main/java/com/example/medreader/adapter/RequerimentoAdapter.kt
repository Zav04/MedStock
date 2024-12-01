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

class RequerimentoAdapter(
    private val context: Context,
    private val requerimentos: List<Requerimento>,
    private val pedidosUrgentesPendentes: Boolean
) : RecyclerView.Adapter<RequerimentoAdapter.ViewHolder>() {

    class ViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val requerimentoId: TextView = itemView.findViewById(R.id.requerimentoId)
        val urgente: TextView = itemView.findViewById(R.id.urgente)
        val btnComecarScan: Button = itemView.findViewById(R.id.btnComecarScan)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_requerimento, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val requerimento = requerimentos[position]

        holder.requerimentoId.text = "Requerimento: ${requerimento.requerimento_id}"
        if (requerimento.urgente) {
            holder.urgente.visibility = View.VISIBLE
            holder.urgente.text = "Urgente!"
            holder.urgente.setTextSize(TypedValue.COMPLEX_UNIT_SP, 18f)
            holder.urgente.setTypeface(null, Typeface.BOLD)
            holder.btnComecarScan.isEnabled = true
        } else {
            holder.urgente.visibility = View.GONE
            holder.btnComecarScan.isEnabled = !pedidosUrgentesPendentes
        }

        holder.btnComecarScan.setOnClickListener {
            val intent = Intent(context, ScanActivity::class.java)
            intent.putExtra("requerimentoId", requerimento.requerimento_id)
            context.startActivity(intent)
        }

    }
    override fun getItemCount(): Int = requerimentos.size
}