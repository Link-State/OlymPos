package com.kmyth.olympos

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.kmyth.olympos.ui.theme.OlymPosTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            OlymPosTheme {
                // A surface container using the 'background' color from the theme
                Login(modifier = Modifier.fillMaxSize())
            }
        }
    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier,
        color = MaterialTheme.colorScheme.primary
    ) {
        Text(
            text = "Hello $name!",
            modifier = modifier
        )
    }
}

@Composable
private fun Login(modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier,
        color = MaterialTheme.colorScheme.background
    ) {
        Greeting("OlymPos")
    }
}

@Preview(showBackground = true)
@Composable
fun Preview() {
    OlymPosTheme {
        Login(modifier = Modifier.fillMaxSize())
    }
}