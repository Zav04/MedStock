package com.example.medreader

import android.content.Intent
import android.os.Bundle
import android.text.method.HideReturnsTransformationMethod
import android.text.method.PasswordTransformationMethod
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.medreader.connection.RetrofitClient
import com.example.medreader.models.LoginRequest
import com.example.medreader.models.LoginResponse
import retrofit2.Call

class LoginActivity : AppCompatActivity() {

    private lateinit var usernameEditText: EditText
    private lateinit var passwordEditText: EditText
    private lateinit var loginButton: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var showPasswordButton: ImageButton

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        usernameEditText = findViewById(R.id.username)
        passwordEditText = findViewById(R.id.password)
        loginButton = findViewById(R.id.login_button)
        progressBar = findViewById(R.id.progressBar)
        showPasswordButton = findViewById(R.id.show_password_button)

        showPasswordButton.setOnClickListener {
            togglePasswordVisibility()
        }

        loginButton.setOnClickListener {
            val username = usernameEditText.text.toString().trim()
            val password = passwordEditText.text.toString()

            if (username.isBlank() || password.isBlank()) {
                Toast.makeText(this, "Preencha todos os campos!", Toast.LENGTH_SHORT).show()
            } else {
                performLogin(username, password)
            }
        }
    }

    private fun performLogin(username: String, password: String) {
        progressBar.visibility = View.VISIBLE

        val loginRequest = LoginRequest(username, password)

        val call = RetrofitClient.loginApi.loginUser(loginRequest)
        call.enqueue(object : retrofit2.Callback<LoginResponse> {
            override fun onResponse(call: Call<LoginResponse>, response: retrofit2.Response<LoginResponse>) {
                progressBar.visibility = View.GONE
                if (response.isSuccessful) {
                    val loginResponse = response.body()
                    if (loginResponse?.response == true) {
                        val userId = loginResponse.data?.utilizador_id
                        if (userId != null) {
                            val sharedPreferences = getSharedPreferences("user_prefs", MODE_PRIVATE)
                            val editor = sharedPreferences.edit()
                            editor.putInt("user_id", userId)
                            editor.apply()
                        }
                        val intent = Intent(this@LoginActivity, RequerimentosActivity::class.java)
                        startActivity(intent)
                        finish()
                    } else {
                        Toast.makeText(this@LoginActivity, loginResponse?.error ?: "Erro ao realizar login.", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    Toast.makeText(this@LoginActivity, "Erro: ${response.message()}", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<LoginResponse>, t: Throwable) {
                progressBar.visibility = View.GONE
                Toast.makeText(this@LoginActivity, "Erro de conexão: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }

    private fun togglePasswordVisibility() {
        val start = passwordEditText.selectionStart
        val end = passwordEditText.selectionEnd

        if (passwordEditText.transformationMethod == PasswordTransformationMethod.getInstance()) {
            passwordEditText.transformationMethod = HideReturnsTransformationMethod.getInstance()
            showPasswordButton.setImageResource(R.drawable.ic_eye_open)
        } else {
            passwordEditText.transformationMethod = PasswordTransformationMethod.getInstance()
            showPasswordButton.setImageResource(R.drawable.ic_eye_close)
        }
        passwordEditText.setSelection(start, end)
    }

}