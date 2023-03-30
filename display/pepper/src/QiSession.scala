import scalajs.js
import scala.scalajs.js.annotation.JSGlobal

@js.native
trait QiSession extends js.Object {
  def service(service: String): js.Promise[js.Dynamic] = js.native
}

@JSGlobal("QiSession")
@js.native
def qiSession(
  connectCallback: js.Function1[QiSession, Unit] = js.native,
  disconnectCallback: js.Function0[Unit] = js.native,
  hostname: String = js.native
): Unit = js.native

