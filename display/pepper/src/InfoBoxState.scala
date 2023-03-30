import scalajs.js
import org.scalajs.dom.XMLHttpRequest
import org.scalajs.dom.{document, html, window}
import org.scalajs.dom.CanvasRenderingContext2D
import floors.Floor
import scala.scalajs.js.timers._

class InfoBoxState(canvas: html.Canvas):

  var saying = ""
  var sayingBase = ""

  var drawTimer: Option[SetTimeoutHandle] = None


  def drawSaying(c2d: CanvasRenderingContext2D) =
    val maxWidth = 40
    var sayingCp = saying
    
    val strs = collection.mutable.Buffer[String]()
    while (sayingCp.length > 0) {
      var cStr = ""
      while (cStr.length <= maxWidth && sayingCp.length > 0)
        cStr += sayingCp.takeWhile(_ != ' ')
        sayingCp = sayingCp.dropWhile(_ != ' ').tail
        cStr += " "
      strs += cStr
    }

    val maxLines = 7

    val lineSpacing = 0.19 * canvas.height / maxLines
    val firstLine = canvas.height * 0.83 + (canvas.height * 0.18 - lineSpacing * (strs.length min maxLines)) / 2
    println(s"Strs: $strs")
    val fill = c2d.createRadialGradient(
      canvas.width/2, canvas.height/2, canvas.width/8,
      canvas.width/2, canvas.height/2, canvas.width/2,
    )
    fill.addColorStop(0, "rgb(25, 102, 153)")
    fill.addColorStop(1, "rgb(0, 25, 76)")
    var firstLoop = true
    def drawTextProcedural(i: Double): Unit = {
      c2d.save()
      c2d.beginPath()
      c2d.moveTo(canvas.width * 0.605, canvas.height * 0.805)
      c2d.lineTo(canvas.width * 0.605, canvas.height * 0.995)
      c2d.lineTo(canvas.width * 0.995, canvas.height * 0.995)
      c2d.lineTo(canvas.width * 0.995, canvas.height * 0.805)
      c2d.closePath()
      c2d.clip()
      c2d.fillStyle = fill
      c2d.fillRect(canvas.width * 0.605, canvas.height * 0.805, canvas.width * 0.39, canvas.height * 0.19)
      c2d.fillStyle = "white"
      for ((str, idx) <- strs.zipWithIndex) {
        c2d.font = "24px Barlow"
        c2d.textAlign = "center"
        c2d.fillText(str, canvas.width * 0.8, firstLine + lineSpacing * idx - i * lineSpacing, canvas.width * 0.375)
      }
      c2d.restore()
      val timeout = if (firstLoop) 2650 else 650
      firstLoop = false
      if (i < strs.size - maxLines)
        drawTimer = Some(setTimeout(timeout)(drawTextProcedural(i + 0.25)))
    }
    drawTextProcedural(0)


  def startSayingUpdate(): Unit =
    val xhr = new XMLHttpRequest()
    xhr.open("GET", s"${PiAddr}/saying")
    xhr.timeout = 2500
    xhr.onload = {e =>
      if xhr.status == 200 then
        val resp = xhr.responseText
        if (resp != sayingBase)
          println("New Timeout!!")
          drawTimer.foreach(clearTimeout)
          drawTimer = None
          sayingBase = resp
          saying = resp.split(" ").filterNot(Seq('*', '#') contains _.headOption.getOrElse('\u0000')).mkString(" ")
          drawSaying(canvas.getContext("2d").asInstanceOf[CanvasRenderingContext2D])
      else println("Failed")
      setTimeout(ReqTimeout)(startSayingUpdate())
    }
    xhr.ontimeout = {_ => setTimeout(ReqTimeout)(startSayingUpdate())}
    xhr.send()
