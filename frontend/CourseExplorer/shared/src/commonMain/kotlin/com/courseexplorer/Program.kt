package com.courseexplorer

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class Program(val link: String = "",
                   @SerialName("program_name")
                   val programName: String = "",
                   val description: String = "",
                   val university: String = "",
                    val id: Int)
{
}