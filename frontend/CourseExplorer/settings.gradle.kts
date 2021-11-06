rootProject.name = "CourseExplorer"

pluginManagement {
    repositories {
        google()
        gradlePluginPortal()
        mavenCentral()
        maven("https://maven.pkg.jetbrains.space/public/p/compose/dev")
    }
}

include(":shared")
//include(":desktopApp")
include(":webApp")
