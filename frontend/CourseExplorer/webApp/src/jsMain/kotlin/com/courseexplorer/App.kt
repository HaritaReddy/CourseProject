package com.courseexplorer

import androidx.compose.runtime.*
import kotlinx.browser.window
import org.jetbrains.compose.web.attributes.InputType
import org.jetbrains.compose.web.attributes.placeholder
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
    onItemClicked: (String) -> Unit){
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

    Div({classes("courseList")}){
        Ul {
            for (currentCourse in currentState.courseList){
                Li({
                    onClick {
                        onItemClicked(currentCourse.link) //maybe use course id instead
                    }
                }) {
                    Text(currentCourse.shortDescription())
                }
            }
        }
        Ul {
            for (currentProgram in currentState.programList){
                Li {
                    Text(currentProgram.programName)
                    Text(currentProgram.link)
                }
            }
        }
    }
}

@Composable
fun DetailScreen(currentState: ViewState){

    val newURL = with(window.location){
        "${protocol}//${host}/${currentState.courseDetail!!.link}"
    }
    window.history.pushState(currentState.pageType, "${currentState.courseDetail!!.link} course details", newURL)

    Text("Hello world ${currentState.courseDetail!!.link}")
}