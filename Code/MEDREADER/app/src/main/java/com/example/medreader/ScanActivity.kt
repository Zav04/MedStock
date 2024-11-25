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
import com.example.medreader.models.ItemLido


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

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_scan)

        btnVoltar = findViewById(R.id.btnVoltar)
        btnFinalizar = findViewById(R.id.btnFinalizar)
        scannerView = findViewById(R.id.scanner_view)
        recyclerViewItensPedido = findViewById(R.id.recyclerViewItensPedido)
        recyclerViewItensLidos = findViewById(R.id.recyclerViewItensLidos)
        recyclerViewItensPedido.layoutManager = LinearLayoutManager(this)
        recyclerViewItensPedido.adapter = ItemPedidoAdapter(itemPedidoList)
        recyclerViewItensLidos.layoutManager = LinearLayoutManager(this)
        recyclerViewItensLidos.adapter = ItemLidoAdapter(itemLidosList)
        pausedSymbol = findViewById(R.id.pausedSymbol)

        simulateItensPedido()
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

    // ITENS SIMULADOS
    private fun simulateItensPedido() {
        itemPedidoList.add(ItemPedido("Medicamento A", 10, "Medicamento"))
        itemPedidoList.add(ItemPedido("Material B", 5, "Material"))
        itemPedidoList.add(ItemPedido("Vacina C", 3, "Vacina"))
        recyclerViewItensPedido.adapter?.notifyDataSetChanged()
    }

    private fun processarQRCode(qrCode: String) {
        val existingItem = itemPedidoList.find { it.nome_item == qrCode }

        if (existingItem == null) {
            dialogoItemNaoExiteLista()
        } else {
            val existingLido = itemLidosList.find { it.nome_item == qrCode }

            if (existingLido != null) {
                Toast.makeText(this, "Item já foi lido.", Toast.LENGTH_SHORT).show()
            } else {
                itemLidosList.add(ItemLido(qrCode, 1))
                recyclerViewItensLidos.adapter?.notifyDataSetChanged()
                Toast.makeText(this, "QR Code Lido: $qrCode", Toast.LENGTH_SHORT).show()
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