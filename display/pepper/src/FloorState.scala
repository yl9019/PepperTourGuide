import scalajs.js
import org.scalajs.dom.XMLHttpRequest
import org.scalajs.dom.{document, html, window}
import org.scalajs.dom.CanvasRenderingContext2D
import floors.Floor
import scala.scalajs.js.timers._

class FloorState(canvas: html.Canvas):
  private var _lvl: Option[Int] = None
  def lvl: Option[Int] = _lvl
  def lvl_=(x: Option[Int]) =
    _lvl = x

  var floorTransition = 1.0

  def currentFloor = floorTransition
  ///var currentFloor = 6.0

  var px: Option[Double] = None
  var py: Option[Double] = None

  val dps = 0.25

  def floorUpdate(): Unit =
    lvl.foreach(llvl =>
      if ((floorTransition - llvl).abs > 0.0001) {
        println(s"Floor Transition: $floorTransition => $llvl")
        floorTransition += dps * (llvl - floorTransition).sign
        updateCnv(this, canvas)
      } else floorTransition = llvl
    )
    

  def startFloorUpdate(): Unit =
    val xhr = new XMLHttpRequest()
    xhr.timeout = 2500
    xhr.open("GET", s"${PiAddr}/floor")
    xhr.onload = {e =>
      if xhr.status == 200 then
        val resp = xhr.responseText.toIntOption
        if resp.isDefined && resp != lvl then
          px = None
          py = None
          lvl = resp
      else println("Failed")
      setTimeout(ReqTimeout)(startFloorUpdate())
    }
    xhr.ontimeout = {e => setTimeout(ReqTimeout)(startFloorUpdate())}
    xhr.send()

  def startPositionUpdate(): Unit =
    val xhr = new XMLHttpRequest()
    xhr.timeout = 2500
    xhr.open("GET", s"${PiAddr}/position")
    xhr.onload = {e =>
      if xhr.status == 200 then
        xhr.responseText.split(";").map(_.toDoubleOption) match {
          case Array(npx, npy) if npx == px && npy == py => ()
          case Array(Some(npx), Some(npy)) =>
            px = Some(npx)
            py = Some(npy)
            updateCnv(this, canvas)
          case _ => 
        }
      else println("Failed")
      setTimeout(ReqTimeout)(startPositionUpdate())
    }
    xhr.ontimeout = {e => setTimeout(ReqTimeout)(startPositionUpdate())}
    xhr.send()

  def offsetForFloor(f: Int): Double =
    if (f == currentFloor) 0d
    else
      val d = ((f - currentFloor).abs min 1) * 3 // 0..1
      if (d >= 1) (f - currentFloor + (f - currentFloor).sign * d) / 10d
      else (f - currentFloor + (f - currentFloor).sign * 4) / 10d
      (f - currentFloor + (f - currentFloor).sign * d) / 10d

  def fillForFloor(f: Int): String =
    val alpha = 0.25 - (f - currentFloor).abs * 0.1875 max 0.0625
    println(s"Alpha floor $f: $alpha")
    s"rgba(51, 102, 153, $alpha)"

  def strokeForFloor(f: Int): String =
    val alpha = 0.75 - (f - currentFloor).abs * 0.5 max 0.25
    val red = (255 * (1 - (f - currentFloor).abs / 11d)).toInt
    s"rgba(0, $red, 255, $alpha)"
  
  val scaleX = 81d * canvas.height * 0.0075
  val scaleY = 81d * canvas.height * 0.0075

  def drawInfoBox(c2d: CanvasRenderingContext2D) =
    println(s"Drawing floor $currentFloor")
    c2d.save()
    c2d.translate(0, 125)
    floors.Floor.floors.minBy(fl => (currentFloor - fl.num).abs).drawInfoBox(c2d)  
    c2d.restore()

  def drawFloors(c2d: CanvasRenderingContext2D) =
    for (floor <- Floor.floors)
      c2d.save()
      c2d.translate(canvas.width * 0.15, canvas.height * 0.05)
      c2d.scale(scaleX , -scaleY)
      val vOffset = offsetForFloor(floor.num)
      c2d.translate(0, vOffset)
      c2d.transform(0.707, -0.409, 0.707, 0.409, 0, -0.816)
      c2d.lineWidth = 0.01
      c2d.shadowBlur = 10
      c2d.scale(-1, 1)
      c2d.translate(-0.5, 0)
      c2d.strokeStyle = strokeForFloor(floor.num)
      c2d.shadowColor = "white"
      c2d.lineWidth = 0.01
      for (room <- floor.rooms)
        println(s"Floor ${floor.num} room ${room}")
        val (x,y) = room.path.headOption.getOrElse(0d, 0d)
        c2d.beginPath()
        c2d.moveTo(x, y)
        for ((x1, y1) <- room.path.tail)
          c2d.lineTo(x1, y1)
        c2d.closePath()
        c2d.stroke()
        c2d.lineWidth = 0.005
        //c2d.fillStyle = fillForFloor(floor.num)
        //c2d.fill()

      c2d.font = "0.15px Barlow"
      c2d.textAlign = "center"
      //c2d.textBaseline = "top"
      println(s"num: ${floor.num}, c: $currentFloor")
      if (floor.num == currentFloor && currentFloor == 6)
        println(s"Px: $px, Py: $py")  
        if( px.isDefined && py.isDefined) {
          c2d.strokeStyle = "red"
          c2d.shadowColor = "red"
          c2d.beginPath()
          c2d.lineWidth = 0.01
          val (xpx, xpy) = floor.transposePosition(px.get, py.get)
          println(s"Px: $xpx, py: $xpy")
          c2d.arc(xpx + 0.085, -xpy + 0.15, 0.0075, 0, 360)
          //c2d.arc(0.155, 0.16, 0.0075, 0, 360)
          c2d.stroke()
      }
      c2d.fillStyle = strokeForFloor(floor.num) 
      c2d.shadowBlur = 10 
      c2d.translate(0.375, 0)
      c2d.scale(-1, -1)
      // Env is pepper
      if (window.screen.availWidth > 1200) {
        c2d.fillText(s"${floor.num}", 0.215, 0.15, 1) 
      } else {
        if floor.num < 10 then
          c2d.fillText(s"${floor.num}", 0.415, 0.15, 1) 
        else
          c2d.fillText(s"${floor.num / 10}", 0.375, 0.15, 1) 
          c2d.fillText(s"${floor.num % 10}", 0.455, 0.15, 1) 
      }
      println(s"Floor ${floor.num} style: ${c2d.strokeStyle}")
      c2d.restore()
