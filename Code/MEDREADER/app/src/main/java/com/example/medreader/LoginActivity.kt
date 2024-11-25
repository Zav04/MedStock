package com.example.medreader

import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.text.method.HideReturnsTransformationMethod
import android.text.method.PasswordTransformationMethod
import android.view.View
import android.view.inputmethod.EditorInfo
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class LoginActivity : AppCompatActivity() {

    private lateinit var usernameEditText: EditText
    private lateinit var passwordEditText: EditText
    private lateinit var loginButton: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var showPasswordButton: ImageButton

    // Código para solicitação de permissão
    private val CAMERA_PERMISSION_REQUEST_CODE = 100

    // Credenciais
    private val validUsername = "123"
    private val validPassword = "123"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        usernameEditText = findViewById(R.id.username)
        passwordEditText = findViewById(R.id.password)
        loginButton = findViewById(R.id.login_button)
        progressBar = findViewById(R.id.progressBar)
        showPasswordButton = findViewById(R.id.show_password_button)

        usernameEditText.setOnEditorActionListener { _, actionId, _ ->
            if (actionId == EditorInfo.IME_ACTION_NEXT) {
                passwordEditText.requestFocus()
                return@setOnEditorActionListener true
            }
            false
        }

        showPasswordButton.setOnClickListener {
            togglePasswordVisibility()
        }

        loginButton.setOnClickListener {
            progressBar.visibility = View.VISIBLE

            val username = usernameEditText.text.toString()
            val password = passwordEditText.text.toString()

            if (username.isBlank() || password.isBlank()) {
                Toast.makeText(this, "Preencha todos os campos!", Toast.LENGTH_SHORT).show()
                progressBar.visibility = View.GONE
            } else {
                if (username == validUsername && password == validPassword) {
                    Toast.makeText(this, "Login realizado com sucesso!", Toast.LENGTH_SHORT).show()
                    val intent = Intent(this, RequerimentosActivity::class.java)
                    startActivity(intent)
                    finish()
                } else {
                    Toast.makeText(this, "Credenciais inválidas!", Toast.LENGTH_SHORT).show()
                    progressBar.visibility = View.GONE
                }
            }
        }
        checkCameraPermission()
    }

    private fun togglePasswordVisibility() {
        if (passwordEditText.transformationMethod == PasswordTransformationMethod.getInstance()) {
            passwordEditText.transformationMethod = HideReturnsTransformationMethod.getInstance()
            showPasswordButton.setImageResource(R.drawable.ic_eye_open)
        } else {
            passwordEditText.transformationMethod = PasswordTransformationMethod.getInstance()
            showPasswordButton.setImageResource(R.drawable.ic_eye_close)
        }
    }

    // Função para verificar e solicitar a permissão da câmera
    private fun checkCameraPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.CAMERA)
                != PackageManager.PERMISSION_GRANTED
            ) {
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(android.Manifest.permission.CAMERA),
                    CAMERA_PERMISSION_REQUEST_CODE
                )
            }
        }
    }
}




//    // Interface Retrofit para o login
//    interface APIService {
//        @POST("MedStock_Login/")
//        fun login(@Body loginRequest: LoginRequest): Call<LoginResponse>
//    }
//
//    // Dados para enviar ao backend
//    data class LoginRequest(val email: String, val password: String)
//    data class LoginResponse(val response: Boolean, val error: String?, val data: Any?)
//
//    private fun createRetrofit(): APIService {
//        val retrofit = Retrofit.Builder()
//            .baseUrl("http://127.0.0.1:8000")
//            .addConverterFactory(GsonConverterFactory.create())
//            .build()
//        return retrofit.create(APIService::class.java)
//    }
//
//    private fun performLogin(email: String, password: String) {
//        val apiService = createRetrofit()
//        val loginRequest = LoginRequest(email, password)
//
//        // Chamada ao backend para realizar o login
//        apiService.login(loginRequest).enqueue(object : Callback<LoginResponse> {
//            override fun onResponse(call: Call<LoginResponse>, response: Response<LoginResponse>) {
//                progressBar.visibility = View.GONE
//
//                if (response.isSuccessful && response.body()?.response == true) {
//                    // Se o login for bem-sucedido, redireciona para a atividade QRScan
//                    val intent = Intent(this@LoginActivity, QRScanActivity::class.java)
//                    startActivity(intent)
//                    finish()
//                } else {
//                    // Exibe a mensagem de erro
//                    Toast.makeText(this@LoginActivity, response.body()?.error ?: "Erro desconhecido", Toast.LENGTH_SHORT).show()
//                }
//            }
//
//            override fun onFailure(call: Call<LoginResponse>, t: Throwable) {
//                progressBar.visibility = View.GONE
//                Toast.makeText(this@LoginActivity, "Erro de conexão: ${t.message}", Toast.LENGTH_SHORT).show()
//            }
//        })
//    }
//}