import org.scalajs.dom.html
import org.scalajs.dom.KeyboardEvent
import org.scalajs.dom.KeyCode
import org.scalajs.dom.XMLHttpRequest

class InputHandler(input: html.Input):
  def hidden = input.style.visibility == "hidden"
  def clearInput(): Unit =
    input.value = ""
    input.style.visibility = "hidden"
  def showInput(): Unit =
    input.style.visibility = "visible"
    input.focus()
  input.onkeydown = {(e: KeyboardEvent) =>
    if (e.keyCode == KeyCode.Enter) {
      val xhr = new XMLHttpRequest()
      xhr.timeout = 5000
      xhr.open("POST", s"${PiAddr}/input")
      xhr.send(input.value)
      println(s"Posted ${input.value}")
      clearInput()
    }  
  }
