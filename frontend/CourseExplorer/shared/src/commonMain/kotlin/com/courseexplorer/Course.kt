package com.courseexplorer

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class Course(
    val university: String = "",
    val link: String = "",
    @SerialName("course_content")
    val courseDescription: String = "",
) {
    fun shortDescription(): String {
        return if (courseDescription.isNotEmpty()) courseDescription.substring(0..50) + Typography.ellipsis else ""
    }
}
