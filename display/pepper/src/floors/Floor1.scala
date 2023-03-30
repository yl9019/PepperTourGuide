package floors

import org.scalajs.dom.CanvasRenderingContext2D

object Floor1 extends Floor(1):
  override val Scale = 20d / 950d // 20m
  val _rooms = Seq[Poly](
    Poly((300,125), (735,125), (735,235), (825,235), (825,115), (1195,115), (1195,0), (3755,0), (3755,1285), (1195,1285), (1195,1335), (315,1335), (315,1095), (250,1095), (250,765), (315,765), (315,320), (300,320)      
    )
  )

  def drawInfoBox(c2d: CanvasRenderingContext2D) =
    c2d.font = "52px Barlow"
    c2d.textAlign = "left"
    c2d.fillStyle = "white"
    c2d.fillText("Floor 1", c2d.canvas.width * 0.6 + 30, 62, 1000)
    c2d.font = "38px Barlow"
    c2d.fillText("Home to:", c2d.canvas.width * 0.6 + 30, 112, 1000)
    c2d.font = "32px Barlow"
    c2d.fillText("· 1st and 2nd year labs", c2d.canvas.width * 0.6 + 30, 172, 1000)
    c2d.fillText("· EEE Stores", c2d.canvas.width * 0.6 + 30, 218, 1000)
    c2d.fillText("· Reprographics", c2d.canvas.width * 0.6 + 30, 264, 1000)

