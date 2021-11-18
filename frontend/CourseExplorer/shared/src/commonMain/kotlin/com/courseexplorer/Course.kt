package com.courseexplorer

import kotlinx.serialization.Serializable

@Serializable
data class Course(
    val id: String = "",
    val courseNumber: String = "",
    val courseDescription: String = "",
) {
    fun shortDescription(): String {
        return if (courseDescription.isNotEmpty()) courseDescription.substring(0..30) + Typography.ellipsis else ""
    }
}
