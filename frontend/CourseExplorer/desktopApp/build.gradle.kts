import org.jetbrains.compose.compose
import org.jetbrains.compose.desktop.application.dsl.TargetFormat
import org.jetbrains.compose.jetbrainsCompose

plugins {
    kotlin("multiplatform") // kotlin("jvm") doesn't work well in IDEA/AndroidStudio (https://github.com/JetBrains/compose-jb/issues/22)
    id("org.jetbrains.compose") version Versions.desktopCompose
}

kotlin {
    jvm {
        withJava()
    }

    sourceSets {
        named("jvmMain") {
            dependencies {
                implementation(compose.desktop.currentOs)
                implementation(compose.web.core) //for web
                implementation(compose.web.svg) //for web
                implementation(compose.runtime)
                //implementation(project(":shared:domain"))
                //implementation(project(":common:database"))
                //implementation(project(":common:root"))
                //implementation(project(":common:compose-ui"))
            }
        }
    }
}

compose.desktop {
    application {
        mainClass = "com.reunionize.MainKt"

        nativeDistributions {
            targetFormats(TargetFormat.Dmg, TargetFormat.Msi, TargetFormat.Deb)
            packageName = "Reunionize"
            packageVersion = "1.0.0"

            windows {
                menuGroup = "Reunionize"
                // see https://wixtoolset.org/documentation/manual/v3/howtos/general/generate_guids.html
                upgradeUuid = "BF9CDA6A-1391-46D5-9ED5-383D6E68CCEB"
            }
        }
    }
}