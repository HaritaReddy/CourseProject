package com.courseexplorer

import io.ktor.client.*
import io.ktor.client.features.json.*
import io.ktor.client.features.json.serializer.*
import io.ktor.client.request.*
import kotlin.collections.get

class BackendClient {

    private val client = HttpClient(){
        install(JsonFeature){
            serializer = KotlinxSerializer()
        }
    }
   // private val address = Url("https://cors-test.appspot.com/test")

    suspend fun init(){
        //temporary function that kicks off the backend data builds
        client.post<Unit>(path = "/init")
    }

    suspend fun search(term: String, maxResults: Int): List<String> {

        val result: List<String> = client.get(path = "/search") {
            parameter("q", term)
            parameter("k", maxResults)
        }

        return result
    }

    suspend fun recommend(term: String): List<String>{
        val result: List<String> = client.get(path = "/recommend") {
            parameter("q", term)
        }
        return result
    }
}