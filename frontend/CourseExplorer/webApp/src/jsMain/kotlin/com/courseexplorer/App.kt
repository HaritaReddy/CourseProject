package com.courseexplorer

import androidx.compose.runtime.*
import kotlinx.browser.window
import org.jetbrains.compose.web.attributes.ATarget
import org.jetbrains.compose.web.attributes.InputType
import org.jetbrains.compose.web.attributes.placeholder
import org.jetbrains.compose.web.attributes.target
import org.jetbrains.compose.web.css.*
import org.jetbrains.compose.web.dom.*
import org.jetbrains.compose.web.renderComposable

fun main() {
    val viewModel = MainViewModel()
    window.onpopstate =  {
        //https://www.codegrepper.com/code-examples/javascript/onpopstate+mobile

        println("my state = ${it.state}")
        if(it.state == null){
            //null state equal home page for now
            viewModel.navigateBackHome()
        }
    }

    renderComposable(rootElementId = "root") {
        val currentState by viewModel.viewStates.collectAsState()
        when(currentState.pageType){
            PageType.HOME -> HomeScreen(currentState, {viewModel.clearSearch()}, {viewModel.fetchResults(it, 20)}, {viewModel.navigateToDetails(it)})
            PageType.DETAIL -> DetailScreen(currentState)
        }

    }
}

@Composable
fun HomeScreen(
    currentState: ViewState,
    onClearClicked: () -> Unit,
    onSubmitClicked: (String) -> Unit,
    onCourseClicked: (Course) -> Unit){
    var searchTerm : String by  remember { mutableStateOf("")}
    Div({
        classes("topnav")
    }) {
        Input(type = InputType.Text){
            id("searchInput")
            value(searchTerm)
            placeholder("Enter Search Term.....")
            onInput {
                searchTerm = it.value
            }
            style {
                width(600.px)
                height(30.px)
            }
        }
        Button({
            onClick {
                searchTerm = ""
                onClearClicked()
            }
        }){
            Text("Clear")
        }

        Button({onClick {
            println("Search Clicked")
            onSubmitClicked(searchTerm) }}){
            Text("Submit")
        }
    }

    Div({classes("courses")}){
        Br()
        if (currentState.universities.isNotEmpty()){
            B {
                Text("Courses")
            }
        }
        Ul {
            for ((index, university) in currentState.universities.withIndex()){
                Li {
                    Text(university) // every course should have a university
                    val currentOnCampus = currentState.courseList.filter { it.university == university }
                    val currentMoocs = currentState.moocList.filter { it.university == university }

                    Ul {
                        if (currentOnCampus.isNotEmpty()){
                            Li {  Text("On Campus Courses") }
                            Ul {
                                for (course in currentOnCampus){
                                    Li({
                                        onClick {
                                            onCourseClicked(course) //maybe use course id instead
                                        }
                                    }) {
                                        Text(course.shortDescription(100))
                                    }
                                }
                            }
                        }

                        if (currentMoocs.isNotEmpty()){
                            Li {Text("MOOC's")}
                            Ul {
                                for (currentMooc in currentMoocs){
                                    Li({
                                        onClick {
                                            onCourseClicked(currentMooc) //maybe use course id instead
                                        }
                                    }) {
                                        Text(currentMooc.shortDescription(100))
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        Div({classes("recommedprogram")}){
            if (currentState.programList.isNotEmpty()){
                B {
                    Text("Recommended Programs")
                }
            }
            Ul {
                for ((university, programs) in currentState.programList){
                    Li{
                        Text(university)
                        Ul {
                            for (program in programs){
                                Li(/*{
                                    onClick {
                                        onItemClicked(program.link) //maybe use course id instead
                                    }
                                }*/) {
                                    Text(program.programName)
                                    Br()
                                    Text(program.description)
                                    Br()
                                    A(href = program.link, attrs = {
                                        target(ATarget.Blank)
                                    }){
                                        Text( "Visit Home Page")
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun DetailScreen(currentState: ViewState){

    val newURL = with(window.location){
        "${protocol}//${host}/${currentState.courseDetail!!.link.drop(7)}"
    }
    window.history.pushState(currentState.pageType, "${currentState.courseDetail!!.link} course details", newURL)

    Text( currentState.courseDetail!!.university!!)
    P {  }
    Text( currentState.courseDetail!!.courseDescription.dropLast(currentState.courseDetail!!.link.length))
    P {  }
    A(href = currentState.courseDetail!!.link, attrs = {
        target(ATarget.Blank)
    }){
        Text( "Visit Home Page")
    }

}