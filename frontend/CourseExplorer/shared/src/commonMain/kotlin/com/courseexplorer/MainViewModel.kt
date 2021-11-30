package com.courseexplorer

import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.async
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.serialization.builtins.ListSerializer
import kotlinx.serialization.json.Json

class MainViewModel {


    private var backendClient: BackendClient = BackendClient()
    private var currentSelected: String? = null
    private var currentState: ViewState = ViewState(PageType.HOME, emptyList(), emptyList())
    private val previousSearches = mutableListOf<String>()
    private val _viewStates = MutableStateFlow(currentState)
    val viewStates: StateFlow<ViewState> = _viewStates.asStateFlow()


    fun fetchResults(searchTerm: String, maxResults: Int){
       // println("Got search request")
       /* val fakeList = listOf(
            Course(courseNumber = "CS100", courseDescription = "the study of forces, their distribution, and their impact on building structure. Topics include: equilibrium of rigid bodies in two and three dimensions"),
            Course(courseNumber = "ECE100", courseDescription = "This course explores the theoretical and practical foundations of architecture and the built environment. It provides an introduction to the architectural graphic communication skills that architects"),
            Course(courseNumber = "ART509", courseDescription = "Presentations and discussions relative to various areas of architectural and environmental design concerns. May be repeated to a maximum of 15 hours.")
        )*/


        if (previousSearches.size == 0){
            previousSearches.add(searchTerm)
            previousSearches.add(searchTerm)
            previousSearches.add(searchTerm)
        }else{
            previousSearches.add(0, searchTerm)
            previousSearches.removeLast()
        }

        GlobalScope.launch {

            val courseResults = async {
                backendClient.search(searchTerm, maxResults)
            }

            val moocResults = async {
                backendClient.mooc(searchTerm, maxResults)
            }

            val programResults = async {
                backendClient.recommend(previousSearches.toList())
            }


            //println("Got courses from backend: ${courseResults.await()}")
            //println("Got moocs from backend: ${moocResults.await()}")

            val courses = Json.decodeFromString(ListSerializer(Course.serializer()), courseResults.await())
                .sortedWith(compareBy({it.university}, {it.shortDescription(10)}))
            val moocs = Json.decodeFromString(ListSerializer(Course.serializer()), moocResults.await())
                //.sortedWith(compareBy({it.university}, {it.shortDescription(10)}))
            val programs = Json.decodeFromString(ListSerializer(Program.serializer()), programResults.await())
                .sortedBy { it.university }.groupBy { it.university }
            _viewStates.tryEmit(ViewState(PageType.HOME, courses, moocs, programs))
        }
    }

    fun navigateToDetails(id: String){
        currentSelected = id //currently use course number
        currentState = viewStates.value
        //TODO: fetch additional info for course
        val selectedCourse = Course(link = id, courseDescription = "the study of forces, their distribution, and their impact on building structure. Topics include: equilibrium of rigid bodies in two and three dimensions")
        _viewStates.tryEmit(ViewState(PageType.DETAIL, emptyList(), emptyList(), emptyMap(), selectedCourse))
    }

    fun navigateBackHome(){
        _viewStates.tryEmit(currentState)
    }

    fun clearSearch(){
        _viewStates.tryEmit(ViewState(PageType.HOME,emptyList(), emptyList()))
    }
}