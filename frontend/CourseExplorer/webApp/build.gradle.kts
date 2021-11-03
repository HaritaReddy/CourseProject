import org.jetbrains.compose.compose


plugins {
    kotlin("multiplatform") // kotlin("jvm") doesn't work well in IDEA/AndroidStudio (https://github.com/JetBrains/compose-jb/issues/22)
    id("org.jetbrains.compose") version "1.0.0-beta5"
}

kotlin {
    js(IR) {
        browser {
            useCommonJs()
            binaries.executable()
        }
    }

    sourceSets {
        named("jsMain") {
            dependencies {
                implementation(project(":shared"))
                implementation(compose.runtime)
                implementation(compose.web.core)
                implementation(compose.web.widgets)
                implementation(npm("copy-webpack-plugin", "9.0.0"))
                //implementation(npm("@material-ui/icons", "4.11.2"))
            }
        }
    }
}

//workaround for https://youtrack.jetbrains.com/issue/KT-48273
/*rootProject.plugins.withType(org.jetbrains.kotlin.gradle.targets.js.nodejs.NodeJsRootPlugin::class.java) {
    rootProject.the<org.jetbrains.kotlin.gradle.targets.js.nodejs.NodeJsRootExtension>().versions.webpackDevServer.version = "4.0.0-rc.0"
}*/

rootProject.plugins.withType(org.jetbrains.kotlin.gradle.targets.js.nodejs.NodeJsRootPlugin::class.java) {
    rootProject.the<org.jetbrains.kotlin.gradle.targets.js.nodejs.NodeJsRootExtension>().versions.webpackCli.version = "4.9.0"
}
