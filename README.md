# Дорисовка изображения

Дорисовка изображения на базе Stable Diffusion, для исполнения нужны ядра Cuda (видеокарта Nvidea).

Для начала нужно установить все нужные зависимости
```bash
pip install -r requirements.txt
# python3 -m pip install -r requirements.txt
```

Меняем платье на зеленое
```bash
python3 modifier.py --prompt "green dress" --image "misc/original_photo.jpg" --mask "misc/dress_mask.png" --outdir "misc/generated/"
```
ИЛИ мы не знаем что указывать в команду и нужно пояснение
```bash
python3 modifier.py --help
```

.
<img src="/misc/original_photo.jpg" width="220" height="330">
<img src="/misc/dress_mask.png" width="220" height="330">
<img src="/misc/generated/generated-image-1.png" width="220" height="330">

Применение маски работает быстрее в 10 раз на Kotlin чем на Python:
```kotlin
import java.awt.image.BufferedImage
import java.io.File
import java.lang.RuntimeException
import javax.imageio.ImageIO

private fun read(file: String): BufferedImage = try {
    ImageIO.read(File(file))
} catch (ex: Exception) {
    throw RuntimeException("Cannot read $file", ex)
}

val mask = read("mask.jpg")
val original = read("original.jpg")
val source = read("source.jpg")

fun main() {
    for (x in 0 until original.width)
        for (y in 0 until original.height)
            // recolor only white pixels of mask
            if (mask.getRGB(x, y) > -(2 shl (mask.colorModel.pixelSize - 2)))
                original.setRGB(x, y, source.getRGB(x, y))

    ImageIO.write(original, "jpg", System.out)
}
```

build.gradle.kts
```kotlin
plugins {
    kotlin("jvm") version "1.8.21"
}

group = "me.func"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

tasks.withType<Jar> {
    manifest {
        attributes["Main-Class"] = "ApplicationKt"
    }
    configurations["compileClasspath"].forEach { file: File ->
        from(zipTree(file.absoluteFile))
        duplicatesStrategy = DuplicatesStrategy.EXCLUDE
    }
}
```
