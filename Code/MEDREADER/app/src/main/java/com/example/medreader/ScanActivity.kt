package com.example.medreader

import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.journeyapps.barcodescanner.BarcodeView
import com.journeyapps.barcodescanner.DecoderFactory
import com.journeyapps.barcodescanner.DefaultDecoderFactory
import com.example.medreader.adapter.ItemPedidoAdapter
import com.example.medreader.adapter.ItemLidoAdapter
import com.example.medreader.models.ItemPedido
import com.example.medreader.connection.RetrofitClient
import com.example.medreader.models.APIResponse
import com.example.medreader.models.ItemLido
import com.example.medreader.models.Requerimento
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


class ScanActivity : AppCompatActivity() {

    private lateinit var btnVoltar: Button
    private lateinit var btnFinalizar: Button
    private lateinit var scannerView: BarcodeView
    private lateinit var recyclerViewItensPedido: RecyclerView
    private lateinit var recyclerViewItensLidos: RecyclerView
    private val itemPedidoList = mutableListOf<ItemPedido>()
    private val itemLidosList = mutableListOf<ItemLido>()
    private var isScanning: Boolean = false
    private lateinit var pausedSymbol: ImageView
    private var requerimentos: List<Requerimento> = listOf()
    private lateinit var itemLidoAdapter: ItemLidoAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_scan)

        btnVoltar = findViewById(R.id.btnVoltar)
        btnFinalizar = findViewById(R.id.btnFinalizar)
        scannerView = findViewById(R.id.scanner_view)
        recyclerViewItensPedido = findViewById(R.id.recyclerViewItensPedido)
        recyclerViewItensLidos = findViewById(R.id.recyclerViewItensLidos)
        recyclerViewItensPedido.layoutManager = LinearLayoutManager(this)
        recyclerViewItensLidos.layoutManager = LinearLayoutManager(this)
        pausedSymbol = findViewById(R.id.pausedSymbol)
        itemLidoAdapter = ItemLidoAdapter(itemLidosList)
        recyclerViewItensLidos.adapter = itemLidoAdapter

        fetchRequerimentos()
        startScanning()

        val formats = listOf(com.google.zxing.BarcodeFormat.QR_CODE)
        val decoderFactory: DecoderFactory = DefaultDecoderFactory(formats)

        scannerView.decoderFactory = decoderFactory
        scannerView.decodeContinuous { result ->
            if (isScanning) {
                val qrCode = result.text
                processarQRCode(qrCode)
                stopScanning()
            }
        }

        scannerView.setOnClickListener {
            if (!isScanning) {
                startScanning()
            }
        }

        btnVoltar.setOnClickListener {
            finish()
        }

        btnFinalizar.setOnClickListener {
            if (verificarItens()) {
                Toast.makeText(this, "Pedido finalizado com sucesso!", Toast.LENGTH_SHORT).show()
            } else {
                dialogoItensNaoScanneados()
            }
        }
    }

    private fun fetchRequerimentos() {
        val call = RetrofitClient.requeimentosApi.getRequerimentos()
        call.enqueue(object : Callback<APIResponse<List<Requerimento>>> {
            override fun onResponse(
                call: Call<APIResponse<List<Requerimento>>>,
                response: Response<APIResponse<List<Requerimento>>>
            ) {
                if (response.isSuccessful && response.body()?.response == true) {
                    requerimentos = response.body()?.data ?: listOf()
                    val intentRequerimentoId = intent.getIntExtra("requerimentoId", -1)

                    val requerimentoSelecionado = requerimentos.find { it.requerimento_id == intentRequerimentoId }
                    if (requerimentoSelecionado != null) {
                        carregarItensRequerimento(requerimentoSelecionado)
                    } else {
                        Toast.makeText(this@ScanActivity, "Requerimento não encontrado", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    Toast.makeText(this@ScanActivity, "Erro ao carregar os requerimentos", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<APIResponse<List<Requerimento>>>, t: Throwable) {
                Toast.makeText(this@ScanActivity, "Falha na comunicação com o servidor", Toast.LENGTH_SHORT).show()
            }
        })
    }

    private fun carregarItensRequerimento(requerimento: Requerimento) {
        itemPedidoList.clear()

        requerimento.itens_pedidos?.forEach { item ->
            itemPedidoList.add(ItemPedido(item.nome_item, item.codigo, item.quantidade))
        }

        recyclerViewItensPedido.adapter = ItemPedidoAdapter(itemPedidoList)
        recyclerViewItensPedido.adapter?.notifyDataSetChanged()
    }

    private fun processarQRCode(qrCode: String) {
        val existingItem = itemPedidoList.find { it.codigo == qrCode }

        if (existingItem == null) {
            dialogoItemNaoExiteLista()
        } else {
            val existingLido = itemLidosList.find { it.codigo == existingItem.codigo }

            if (existingLido != null) {
                Toast.makeText(this, "Item já foi lido.", Toast.LENGTH_SHORT).show()
            } else {
                val itemLido = ItemLido(existingItem.nome_item, existingItem.codigo, 1)
                itemLidosList.add(itemLido)
                itemLidoAdapter.notifyItemInserted(itemLidosList.size - 1)
                Toast.makeText(this, "QR Code Lido: ${existingItem.nome_item}", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun startScanning() {
        isScanning = true
        scannerView.resume()
        pausedSymbol.visibility = View.GONE
    }

    private fun stopScanning() {
        isScanning = false
        scannerView.pause()
        pausedSymbol.visibility = View.VISIBLE
        Toast.makeText(this, "Scanner parado. Toque no Scan para continuar.", Toast.LENGTH_SHORT).show()
    }

    private fun verificarItens(): Boolean {
        return itemPedidoList.all { pedidoItem ->
            val itemLido = itemLidosList.find { it.nome_item == pedidoItem.nome_item }
            itemLido?.quantidade_lida == pedidoItem.quantidade
        }
    }

    private fun dialogoItensNaoScanneados() {
        val builder = AlertDialog.Builder(this)
        builder.setTitle("Erro")
        builder.setMessage("Não pode finalizar o pedido. Ainda existem itens na lista de pedidos do requerimento que não passaram pelo Scan !!")
        builder.setPositiveButton("OK") { dialog, _ -> dialog.dismiss() }
        builder.show()
    }

    private fun dialogoItemNaoExiteLista() {
        val builder = AlertDialog.Builder(this)
        builder.setTitle("Erro")
        builder.setMessage("O item que deu Scan não está na lista de itens pedidos no requerimento !!")
        builder.setPositiveButton("OK") { dialog, _ -> dialog.dismiss() }
        builder.show()
    }
}