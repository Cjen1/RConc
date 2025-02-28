open Core
type rid = int

type op = Write of string * string | Read of string [@@deriving compare]
type res = Success | Failure of [`Msg of string | `Error of exn]

type recv_callback = rid * res -> unit

type url = Eio.Net.Sockaddr.stream

let x = Some (Invalid_argument "")

module type S = sig
  type mgr

  val submit : mgr -> rid * op -> unit

  val create : sw:Eio.Switch.t -> env: Eio_unix.Stdenv.base -> f:recv_callback -> urls:url list -> id:int -> mgr

  val flush : mgr -> unit
end
