-module(server).
-export([main/1]).

main(_) ->
  inets:start(),
  {ok, Pid} = inets:start(httpd, [
    {port, 5550},
    {server_name,"httpd_test"},
    {server_root,"/home/tm/Script/wwwtest/"},
    {document_root,"/home/tm/Script/wwwtest/htdocs"},
    {bind_address, "localhost"},
    {modules, [handler]}
  ]),
  {ok, Pid},
  register(server_a, self()),
  loop(#{floor => "6", saying => "", pos => "0.0;0.0"}).

loop(Map=#{floor := Floor, saying := Saying, pos := Pos}) ->
  Next = receive
    {put_say, Say} -> Map#{saying => Say};
    {put_floor, NFloor} -> Map#{floor => NFloor};
    {put_pos, NPos} -> Map#{pos => NPos};
    {get_say, From} -> From!{saying, Saying}, Map;
    {get_floor, From} -> From!{floor, Floor}, Map;
    {get_pos, From} -> From!{pos, Pos}, Map
  end,
  io:fwrite("Next: ~p~n", [Next]),
  loop(Next).

