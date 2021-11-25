package com.courseexplorer

import kotlinx.serialization.Serializable

@Serializable
data class Program(val id: String = "",
                   val programName: String = "",
                   val programDescription: String = "",) {
}