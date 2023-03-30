import org.scalajs.dom.{document, html, window, CanvasRenderingContext2D}
import scala.scalajs.js.timers._

//final val PiAddr = "http://localhost:5550"//"http://192.168.0.103:5550"
final val PiAddr = "http://192.168.0.103:5550"

def redrawCnv(floor: FloorState, canvas: html.Canvas): Unit =
  val c2d = canvas.getContext("2d").asInstanceOf[CanvasRenderingContext2D]
  val fill = c2d.createRadialGradient(
    canvas.width/2, canvas.height/2, canvas.width/8,
    canvas.width/2, canvas.height/2, canvas.width/2,
  )
  fill.addColorStop(0, "rgb(25, 102, 153)")
  fill.addColorStop(1, "rgb(0, 25, 76)")
  c2d.fillStyle = fill
  c2d.fillRect(0, 0, canvas.width * 0.59, canvas.height)
  c2d.fillRect(canvas.width * 0.605, 0, canvas.width * 0.39, canvas.height * 0.795)
  floor.drawFloors(c2d)

  floor.drawInfoBox(c2d)

def updateCnv(floor: FloorState, canvas: html.Canvas): Unit =
  println(s"Update wh to ${canvas.clientWidth}, ${canvas.clientHeight}")
  redrawCnv(floor, canvas)

def initCanvas(canvas: html.Canvas) =
  val c2d = canvas.getContext("2d").asInstanceOf[CanvasRenderingContext2D]
  val fill = c2d.createRadialGradient(
    canvas.width/2, canvas.height/2, canvas.width/8,
    canvas.width/2, canvas.height/2, canvas.width/2,
  )
  fill.addColorStop(0, "rgb(25, 102, 153)")
  fill.addColorStop(1, "rgb(0, 25, 76)")
  c2d.fillStyle = fill
  c2d.fillRect(0, 0, canvas.width, canvas.height)
  
  c2d.beginPath()
  c2d.strokeStyle = "white"
  c2d.moveTo(canvas.width * 0.6, canvas.height * 0.8)
  c2d.lineTo(canvas.width, canvas.height * 0.8)
  c2d.stroke()
  c2d.closePath()

  c2d.strokeStyle = "white"
  c2d.lineWidth = 1
  c2d.strokeRect(canvas.width * 0.6, 0, canvas.width * 0.4, canvas.height)

final val ReqTimeout = 250

@main def main =
  val canvas = document.getElementById("main-canvas").asInstanceOf[html.Canvas]
  // Pepper's CSS does not support this
  if (window.screen.availWidth > 1200)
    canvas.style.right = "0"
    canvas.style.left = "auto"
    
  canvas.width = 1280
  canvas.height = 800

  val floor = FloorState(canvas)
  val saying = InfoBoxState(canvas)
  val input =
    InputHandler(document.getElementById("input-hide").asInstanceOf[html.Input])
  input.clearInput()
  window.onclick = {_ =>
    if (input.hidden)
      input.showInput()
    else input.clearInput()
  }
  initCanvas(canvas)
  floor.startFloorUpdate()
  floor.startPositionUpdate()
  saying.startSayingUpdate()
  setInterval(120)(floor.floorUpdate())

  setTimeout(500) {
    updateCnv(floor, canvas)
  }
  /*
  var dps = 0.15

  lazy val timer: SetIntervalHandle = setInterval(250)(updateTimer())

  def updateTimer(): Unit = 
    if (floor.currentFloor >= 6 || floor.currentFloor <= 5) dps *= -1
    floor.currentFloor += dps
    println(floor.currentFloor)
    updateCnv(floor, canvas)

  timer
  */


// cd ~/web_server; escript server.beam
