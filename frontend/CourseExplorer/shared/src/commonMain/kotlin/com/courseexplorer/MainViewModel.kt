package com.courseexplorer

import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.async
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json

class MainViewModel {


    private var backendClient: BackendClient = BackendClient()
    private var currentSelected: String? = null
    private var currentState: ViewState = ViewState(PageType.HOME, emptyList())
    private val _viewStates = MutableStateFlow(currentState)
    val viewStates: StateFlow<ViewState> = _viewStates.asStateFlow()


    fun fetchResults(searchTerm: String, maxResults: Int){
        println("Got search request")
       /* val fakeList = listOf(
            Course(courseNumber = "CS100", courseDescription = "the study of forces, their distribution, and their impact on building structure. Topics include: equilibrium of rigid bodies in two and three dimensions"),
            Course(courseNumber = "ECE100", courseDescription = "This course explores the theoretical and practical foundations of architecture and the built environment. It provides an introduction to the architectural graphic communication skills that architects"),
            Course(courseNumber = "ART509", courseDescription = "Presentations and discussions relative to various areas of architectural and environmental design concerns. May be repeated to a maximum of 15 hours.")
        )*/


        GlobalScope.launch {

            val courseResults = async {
                backendClient.search(searchTerm, maxResults)
            }

            val programResults = async {
                backendClient.recommend(searchTerm)
            }


            println("Got courses from backend: ${courseResults.await()}")
            println("Got progams from backend: ${programResults.await()}")
            /*val courses = courseResults.await().map { Json.decodeFromString<Course>(it) }
            val programs = programResults.await().map { Json.decodeFromString<Program>(it) }


            println("Got courses from backend: $courses")
            println("Got programs from backend: $programs")
            println(" emitting new viewstate from viewmodel")
            _viewStates.tryEmit(ViewState(PageType.HOME, courses, programs))
             */
        }
    }



    fun navigateToDetails(id: String){
        currentSelected = id //currently use course number
        currentState = viewStates.value
        //TODO: fetch additional info for course
        val selectedCourse = Course(courseNumber = id, courseDescription = "the study of forces, their distribution, and their impact on building structure. Topics include: equilibrium of rigid bodies in two and three dimensions")
        _viewStates.tryEmit(ViewState(PageType.DETAIL, emptyList(), emptyList(), selectedCourse))



    }

    fun navigateBackHome(){
        _viewStates.tryEmit(currentState)
    }

    fun clearSearch(){
        _viewStates.tryEmit(ViewState(PageType.HOME,emptyList()))
    }
}