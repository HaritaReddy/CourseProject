package com.courseexplorer

data class ViewState(
    val pageType: PageType,
    val courseList: List<Course>,
    val courseDetail: Course? = null
)
