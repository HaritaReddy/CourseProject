package com.reunionize

import androidx.compose.desktop.DesktopTheme
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.ui.Modifier
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import androidx.compose.ui.window.rememberWindowState
import androidx.compose.material.Text

fun main() {
    application {
        val windowState = rememberWindowState()

        Window(
            onCloseRequest = ::exitApplication,
            state = windowState,
            title = "Todo"
        ) {
            Surface(modifier = Modifier.fillMaxSize()) {
                MaterialTheme {
                    DesktopTheme {

                        Text("Hello Desktop World")
                    }
                }
            }
        }
    }
}