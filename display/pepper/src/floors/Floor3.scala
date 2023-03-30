package floors

import org.scalajs.dom.CanvasRenderingContext2D

object Floor3 extends Floor(3):
  val _rooms = Seq(
    Poly(
      (342,  145),
      (1460, 145),
      (1460, 3670),
      (352,  3670),
      (352,  3270),
      (0,    3270),
      (0,    2270),
      (352,  2270),
      (352,  1285),
      (275,  1285),
      (275,  870),
      (352,  870),
      (352,  325),
      (342,  325),
    ),
    Poly(
      (602, 505),
      (602, 870),
      (275, 870),
      (275, 1285),
      (602, 1285),
      (602, 1320),
      (575, 1320),
      (575, 1620),
      (650, 1620),
      (650, 3290),
      (770, 3290),
      (770, 1620),
      (770, 505),
      (602, 505),
    )
  )

  def drawInfoBox(c2d: CanvasRenderingContext2D) =
    c2d.font = "52px Barlow"
    c2d.textAlign = "left"

    c2d.fillStyle = "white"
    c2d.fillText("Floor 3", c2d.canvas.width * 0.6 + 30, 62, 1000)
    c2d.font = "38px Barlow"
    c2d.fillText("Home to:", c2d.canvas.width * 0.6 + 30, 112, 1000)
    c2d.font = "32px Barlow"
    def drawText(start: Int, text: Seq[String]): Unit =
      text.headOption.foreach(hd => {
        c2d.fillText(hd, c2d.canvas.width * 0.6 + 30, start, 1000)
        drawText(start + 46, text.tail)
      })
    val strs = Seq(
      "· Mens' Toilet",
      "· Undergraduate Computer Room"
    )
    drawText(172, strs)

