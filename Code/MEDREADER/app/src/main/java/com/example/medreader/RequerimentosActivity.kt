package com.example.medreader

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
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

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_requerimentos)
        recyclerView = findViewById(R.id.recyclerViewRequerimentos)
        recyclerView.layoutManager = LinearLayoutManager(this)
        btnAtualizar = findViewById(R.id.btnAtualizar)

        fetchRequerimentos()

        btnAtualizar.setOnClickListener {
            fetchRequerimentos()
        }
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_logout -> {
                val sharedPreferences = getSharedPreferences("user_prefs", MODE_PRIVATE)
                val editor = sharedPreferences.edit()
                editor.clear()
                editor.apply()

                val intent = Intent(this, LoginActivity::class.java)
                startActivity(intent)
                finish()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    override fun onResume() {
        super.onResume()
        fetchRequerimentos()
    }

    private fun fetchRequerimentos() {
        RetrofitClient.requeimentosApi.getRequerimentos().enqueue(object : Callback<APIResponse<List<Requerimento>>> {
            override fun onResponse(
                call: Call<APIResponse<List<Requerimento>>>,
                response: Response<APIResponse<List<Requerimento>>>
            ) {
                if (response.isSuccessful) {
                    val apiResponse = response.body()
                    val requerimentos = apiResponse?.data ?: emptyList()
                    val pedidosUrgentesPendentes = requerimentos.any { it.urgente }
                    val requerimentosReordenados = requerimentos.sortedWith(
                        compareByDescending<Requerimento> { it.urgente }.thenBy { requerimentos.indexOf(it) }
                    )
                    recyclerView.adapter = RequerimentoAdapter(this@RequerimentosActivity, requerimentosReordenados, pedidosUrgentesPendentes)
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