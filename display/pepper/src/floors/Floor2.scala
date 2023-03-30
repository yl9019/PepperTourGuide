package floors

import org.scalajs.dom.CanvasRenderingContext2D

object Floor2 extends Floor(2):
  val _rooms = Seq(
    Poly(
      (342,  145),
      (1460, 145),
      (1460, 980),
      (1310, 980),
      (1310, 1350),
      (1460, 1350),
      (1460, 2175),
      (342,  2175),
      (342,  1285),
      (275,  1285),
      (275,  870),
      (342,  870),
    ),
    Poly(
      (602, 505),
      (602, 870),
      (275, 870),
      (275, 1285),
      (602, 1285),
      (602, 1320),
      (602, 1710),
      (762, 1710),
      (762, 1570),
      (1067, 1570),
      (1067, 1350),
      (1310, 1350),
      (1310, 960),
      (1145, 960),
      (1145, 750),
      (1055, 750),
      (910, 825),
      (880, 750),
      (850, 750),
      (850, 505),
    )
  )
  
  def drawInfoBox(c2d: CanvasRenderingContext2D) =
    c2d.font = "52px Barlow"
    c2d.textAlign = "left"

    c2d.fillStyle = "white"
    val base = 0
    c2d.fillText("Floor 2", c2d.canvas.width * 0.6 + 30, base + 62, 1000)
    c2d.font = "38px Barlow"
    c2d.fillText("Home to:", c2d.canvas.width * 0.6 + 30, base + 112, 1000)
    c2d.font = "32px Barlow"
    def drawText(start: Int, text: Seq[String]): Unit =
      text.headOption.foreach(hd => {
        c2d.fillText(hd, c2d.canvas.width * 0.6 + 30, start, 1000)
        drawText(start + 46, text.tail)
      })
    val strs = Seq(
      "· Mens' Toilet",
      "· Womens' Toilet",
      "· 1st & 2nd year study space",
      "· Lobby",
      "· Digital Energy Demonstrator"
    )
    drawText(base + 172, strs)