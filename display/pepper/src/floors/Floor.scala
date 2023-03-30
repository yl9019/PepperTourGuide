package floors

import org.scalajs.dom.CanvasRenderingContext2D

// Path from 0-1
class Poly(val path: (Double, Double)*)

object Floor:
  val floors = Seq(
    Floor1, 
    Floor2,
    Floor3,
    Floor4,
    Floor5, 
    Floor6,
    Floor7,
    Floor8,
    Floor9,
    Floor10,
    Floor11,
    Floor12
  )

abstract class Floor(val num: Int):
  val rot: Double = 0
  val scale: Double = 1
  final val Width = 63d
  final val Height = 81d
  val Scale = 20d / 1180d
  val _rooms: Seq[Poly]
  lazy val rooms: Seq[Poly] =
    _rooms.map(poly => Poly(poly.path.map((x,y) => (x * Scale / Height, y * Scale / Width)): _*))
  def drawInfoBox(c2d: CanvasRenderingContext2D): Unit
  def transposePosition(x: Double, y: Double): (Double, Double) =
    val nx = (x * math.cos(rot) - y * math.sin(rot)) * scale
    val ny = (y * math.cos(rot) + x * math.sin(rot)) * scale
    (nx, ny)
    