import org.jetbrains.kotlin.gradle.plugin.mpp.KotlinNativeTarget

plugins {
    kotlin("multiplatform")
    kotlin("plugin.serialization")
}

kotlin {
    jvm("desktop")
    js(IR) {
        browser()
    }

    sourceSets {
        val commonMain by getting{
            dependencies {
                implementation("io.ktor:ktor-client-core:1.6.4")
                implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.3.1")


                //implementation(Deps.Kotlinx.serializationJson)
                //implementation(Deps.Ktor.clientCore)
                //implementation(Deps.Ktor.clientJson)
                //implementation(Deps.Ktor.clientSerialization)
            }
        }
        val commonTest by getting {
            dependencies {
                implementation(kotlin("test-common"))
                implementation(kotlin("test-annotations-common"))
            }
        }
        val desktopMain by getting{
            dependencies {
                implementation("io.ktor:ktor-client-okhttp:1.6.4")
            }
        }
        val desktopTest by getting {
            dependencies {
                implementation(kotlin("test-junit"))
                implementation("junit:junit:4.13.2")
            }
        }
        val jsMain by getting{
            dependencies {
                //implementation("io.ktor:ktor-client-js:1.6.4")
            }
        }
        val jsTest by getting
    }
}