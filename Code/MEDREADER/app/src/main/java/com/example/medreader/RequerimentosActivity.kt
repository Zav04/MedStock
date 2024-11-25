package com.example.medreader

import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.medreader.adapter.RequerimentoAdapter
import com.example.medreader.connection.RetrofitClient
import com.example.medreader.models.APIResponse
import com.example.medreader.models.Requerimento
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


class RequerimentosActivity : AppCompatActivity() {
    private lateinit var btnAtualizar: Button
    private lateinit var recyclerView: RecyclerView

    // User que tem tudo
    val userId = 12

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_requerimentos)
        recyclerView = findViewById(R.id.recyclerViewRequerimentos)
        recyclerView.layoutManager = LinearLayoutManager(this)
        btnAtualizar = findViewById(R.id.btnAtualizar)

        fetchRequerimentos(userId)

        btnAtualizar.setOnClickListener {
            fetchRequerimentos(userId)
        }
    }

    private fun fetchRequerimentos(userId: Int) {
        RetrofitClient.api.getRequerimentosByUser(userId).enqueue(object : Callback<APIResponse<List<Requerimento>>> {
            override fun onResponse(
                call: Call<APIResponse<List<Requerimento>>>,
                response: Response<APIResponse<List<Requerimento>>>
            ) {
                if (response.isSuccessful) {
                    val apiResponse = response.body()
                    val requerimentos = apiResponse?.data ?: emptyList()
                    val requerimentosOrdenados = requerimentos.sortedWith(
                        compareByDescending<Requerimento> { it.urgente }
                            .thenBy { it.data_pedido }
                    )
                    recyclerView.adapter = RequerimentoAdapter(this@RequerimentosActivity, requerimentosOrdenados)
                } else {
                    Toast.makeText(
                        this@RequerimentosActivity,
                        "Erro: ${response.message()}",
                        Toast.LENGTH_LONG
                    ).show()
                }
            }
            override fun onFailure(call: Call<APIResponse<List<Requerimento>>>, t: Throwable) {
                Toast.makeText(this@RequerimentosActivity, "Erro: ${t.message}", Toast.LENGTH_LONG).show()
            }
        })
    }
}