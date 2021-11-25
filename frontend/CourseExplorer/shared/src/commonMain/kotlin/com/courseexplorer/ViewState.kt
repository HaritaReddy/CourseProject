package com.courseexplorer

data class ViewState(
    val pageType: PageType,
    val courseList: List<Course>,
    val programList: List<Program> = emptyList(),
    val courseDetail: Course? = null
)
