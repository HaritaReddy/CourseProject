package com.courseexplorer

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class Course(
    val university: String? = null,
    val link: String = "",
    @SerialName("course_content")
    val courseDescription: String = "",
) {
    fun shortDescription(max: Int = 50): String {
        return if (courseDescription.isNotEmpty()) courseDescription.substring(0..max) + Typography.ellipsis else ""
    }
}
