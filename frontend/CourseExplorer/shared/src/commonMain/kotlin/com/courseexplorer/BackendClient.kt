package com.courseexplorer

import io.ktor.client.*
import io.ktor.client.request.*
import kotlin.collections.get

class BackendClient {

    private val client = HttpClient()
   // private val address = Url("https://cors-test.appspot.com/test")

    suspend fun search(term: String, maxResults: Int): List<String>{

        val result: List<String> = client.get(path = "/search") {
            parameter("q", term)
            parameter("k", maxResults)
        }

        return result
    }
}