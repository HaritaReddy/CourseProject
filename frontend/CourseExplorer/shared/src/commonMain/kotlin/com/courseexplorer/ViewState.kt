package com.courseexplorer

data class ViewState(
    val pageType: PageType,
    val courseList: List<Course>,
    val moocList: List<Course>,
    val programList: Map<String, List<Program>> = emptyMap(),
    val universities: List<String>,
    val courseDetail: Course? = null
)
