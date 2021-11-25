package com.courseexplorer

import io.ktor.client.*
import io.ktor.client.features.json.*
import io.ktor.client.features.json.serializer.*
import io.ktor.client.request.*
import kotlin.collections.get

class BackendClient {

    private val client = HttpClient()/*{
        install(JsonFeature){
            serializer = KotlinxSerializer(kotlinx.serialization.json.Json {
                isLenient = true
            })
        }
    }*/
   // private val address = Url("https://cors-test.appspot.com/test")

    suspend fun init(){
        //temporary function that kicks off the backend data builds
        client.post<Unit>(path = "/init")
    }

    suspend fun search(term: String, maxResults: Int): String {
        val result: String = client.get(path = "/search") {
            parameter("q", term)
            parameter("k", maxResults)
        }

        return result
    }

    suspend fun recommend(term: String): String {
        val result: String = client.get(path = "/recommend") {
            parameter("q1", term)
            parameter("q2", "science")
            parameter("q3", "engineering")
        }
        return result
    }
}