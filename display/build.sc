import mill._, scalalib._, scalajslib._, scalajslib.api._

object pepper extends ScalaJSModule {

  def scalaVersion = "3.2.1"
  def scalaJSVersion = "1.13.0"
  def scalacOptions = Seq("-deprecation")
  def ivyDeps = Agg(ivy"org.scala-js:scalajs-dom_sjs1_3:2.2.0")
  def esFeatures = ESFeatures.Defaults.withESVersion(ESVersion.ES5_1)
}
